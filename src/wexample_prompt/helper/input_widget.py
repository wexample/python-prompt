"""Multiline input widget rendered in raw terminal mode.

Stdlib only except wcwidth (already a wexample-prompt dependency).

Layout when ``bordered=True``::

    ────────────────────────────────────────
    > first line
    . second line
    ────────────────────────────────────────
    ? info zone

When ``bordered=False``, the bar and info lines are omitted; only the prefix
lines are rendered.

Keys:
    Enter                            -> submit
    Shift+Enter / Alt+Enter / Ctrl+J -> insert newline
    Backslash + Enter                -> insert newline
    Backspace                        -> delete previous char
    Left / Right                     -> move cursor
    Up / Down                        -> move across lines
    Home / End (or Ctrl+A / Ctrl+E)  -> jump to line start/end
    Ctrl+G                           -> toggle key-trace overlay
    Ctrl+C                           -> abort

Bracketed paste is enabled, so multiline pastes (including emojis and
multi-byte chars) are inserted as a block.
"""

from __future__ import annotations

import select
import shutil
import signal
import sys
import termios
import tty

from wcwidth import wcswidth

CSI = "\x1b["
# Gap allowed between bare ESC and the next byte: short, to disambiguate
# "user pressed Escape" from "Alt+X" or the start of a CSI sequence.
ESC_TIMEOUT = 0.2
# Gap allowed *inside* a CSI / SS3 sequence (after we've already seen
# `\x1b[` or `\x1bO`). Some terminals (gnome-terminal under load, SSH,
# remote sessions) deliver these bytes with a noticeable gap; if we time
# out too early, the final byte (A/B/C/D…) arrives later as a bare key
# and gets inserted into the buffer. No human types `[A` by hand, so a
# generous timeout here is safe.
CSI_TAIL_TIMEOUT = 1.0

KITTY_ON = "\x1b[>1u"
KITTY_OFF = "\x1b[<u"
MOK_ON = "\x1b[>4;2m"  # xterm modifyOtherKeys=2
MOK_OFF = "\x1b[>4;0m"
PASTE_ON = "\x1b[?2004h"
PASTE_OFF = "\x1b[?2004l"
PASTE_START = "\x1b[200~"
PASTE_END = "\x1b[201~"

BAR_CHAR = "─"  # U+2500 BOX DRAWINGS LIGHT HORIZONTAL

DEFAULT_INFO = "Enter=submit | Shift+Enter=newline | Ctrl+G=debug | Ctrl+C=abort"


def cursor_rowcol(buffer: str, cursor: int) -> tuple[int, int]:
    before = buffer[:cursor]
    row = before.count("\n")
    last_nl = before.rfind("\n")
    line_before = before if last_nl == -1 else before[last_nl + 1 :]
    return row, display_width(line_before)


def display_width(s: str) -> int:
    """Width in terminal columns, treating wide chars (emoji/CJK) as 2."""
    w = wcswidth(s)
    return w if w >= 0 else len(s)


def read_csi_tail(prefix: str = "\x1b[") -> str:
    """Read remaining bytes of a CSI sequence until its final byte."""
    seq = prefix
    while True:
        r, _, _ = select.select([sys.stdin], [], [], CSI_TAIL_TIMEOUT)
        if not r:
            break
        c = sys.stdin.read(1)
        seq += c
        if 0x40 <= ord(c) <= 0x7E:
            break
    return seq


def read_key() -> str:
    """Read one logical key, aggregating CSI/SS3 escape sequences."""
    ch = sys.stdin.read(1)
    if ch != "\x1b":
        return ch
    # First byte after ESC: short timeout to disambiguate bare ESC from
    # the start of a CSI/SS3 sequence or an Alt+X combo.
    r, _, _ = select.select([sys.stdin], [], [], ESC_TIMEOUT)
    if not r:
        return "\x1b"
    c2 = sys.stdin.read(1)
    seq = "\x1b" + c2
    if c2 not in "[O":
        return seq
    # Inside CSI/SS3: subsequent bytes may arrive with a noticeable lag
    # on slow / remote terminals — use the longer CSI_TAIL_TIMEOUT so we
    # don't return a half-read `\x1b[` and then mis-handle the trailing
    # `A/B/C/D` as a literal letter typed by the user.
    while True:
        r, _, _ = select.select([sys.stdin], [], [], CSI_TAIL_TIMEOUT)
        if not r:
            break
        c = sys.stdin.read(1)
        seq += c
        if 0x40 <= ord(c) <= 0x7E:
            break
    return seq


def read_paste() -> str:
    """Consume bytes until the bracketed-paste end marker."""
    buf: list[str] = []
    end_len = len(PASTE_END)
    while True:
        buf.append(sys.stdin.read(1))
        if "".join(buf[-end_len:]) == PASTE_END:
            return "".join(buf[:-end_len])


def write(s: str) -> None:
    sys.stdout.write(s)
    sys.stdout.flush()


class InputWidget:
    """Reusable multi-line input widget rendered inline (no full-screen)."""

    # Completion list: rows shown at once (after that, the user keeps typing
    # to filter further).
    COMPLETION_MAX_ROWS = 10

    def __init__(
        self,
        width: int | None = None,
        info: str = DEFAULT_INFO,
        debug: bool = False,
        initial: str = "",
        bordered: bool = True,
        prompt_prefix: str = "> ",
        continuation_prefix: str | None = None,
        completions: list[tuple[str, str]] | None = None,
        width_provider=None,
    ) -> None:
        # An explicit `width` kwarg fixes the widget at that size and disables
        # resize handling. `width_provider` is the "live" source — called on
        # init and on SIGWINCH; if provided it wins over the static fallback.
        self._width_override = width
        self._width_provider = width_provider
        self.width = width or self._read_live_width()
        self.info = info
        self.debug = debug
        self.last_key_trace = ""
        self.buffer = initial
        self.cursor = len(initial)
        self.bordered = bordered
        self.prompt_prefix = prompt_prefix
        # Default continuation prefix: blank spaces matching the prompt width,
        # so wrapped lines stay aligned without a visible marker.
        self.continuation_prefix = (
            continuation_prefix
            if continuation_prefix is not None
            else " " * display_width(prompt_prefix)
        )
        # First-line and continuation prefixes share a single display width to
        # keep cursor math straightforward.
        self._prefix_width = display_width(prompt_prefix)
        # Slash-triggered autocomplete: list of (name, description) tuples.
        # Names typically start with "/" but the widget doesn't enforce it —
        # we only enter completion mode when buffer is "/<word>" (no space,
        # no newline), so empty list ⇒ no completion mode ever.
        self.completions = completions or []
        self._completion_index = 0
        self._rendered = False
        self._cursor_up_to_top = 0
        self._needs_resize = False

    @staticmethod
    def _terminal_width() -> int:
        # Standalone fallback when no width_provider is wired in (used by the
        # demo script and direct InputWidget callers).
        return max(20, shutil.get_terminal_size((80, 20)).columns)

    def render(self) -> None:
        lines = self.buffer.split("\n")
        cur_row, cur_col = cursor_rowcol(self.buffer, self.cursor)

        # Visual rows per logical line (accounting for terminal wrap).
        line_visual_rows = [self._visual_rows_for_line(l) for l in lines]
        # Cursor's visual offset within its own logical line.
        cur_visual_offset = (self._prefix_width + cur_col) // self.width
        cur_visual_col = (self._prefix_width + cur_col) % self.width
        # Cursor visual row from the top of the input area.
        cur_visual_row_from_top = sum(line_visual_rows[:cur_row]) + cur_visual_offset

        if self._rendered:
            if self._cursor_up_to_top > 0:
                write(f"\r{CSI}{self._cursor_up_to_top}A")
            else:
                write("\r")
            write(f"{CSI}J")
        else:
            write("\r")

        if self.bordered:
            bar = BAR_CHAR * self.width
            write(f"{bar}\r\n")

        for i, line in enumerate(lines):
            prefix = self.prompt_prefix if i == 0 else self.continuation_prefix
            write(f"{prefix}{line}\r\n")

        info_rows: list[str] = []
        if self.bordered:
            write(f"{BAR_CHAR * self.width}\r\n")
            info_rows = self._info_rows()
            for j, info_line in enumerate(info_rows):
                if j == len(info_rows) - 1:
                    write(info_line)  # last row: no trailing newline
                else:
                    write(f"{info_line}\r\n")

        # Visual rows between the cursor's visual row and the bottom of what we
        # just printed. Bordered: cursor sits at end of the last info row;
        # non-bordered: cursor sits one row below the last input line.
        rows_below_cursor_in_input = (
            line_visual_rows[cur_row] - 1 - cur_visual_offset
        ) + sum(line_visual_rows[cur_row + 1 :])
        if self.bordered:
            # last info row → climb (info_rows - 1) → climb 1 to bottom bar
            #   → climb 1 more to last input row
            rows_to_climb = rows_below_cursor_in_input + 1 + len(info_rows)
        else:
            # one row below last input row
            rows_to_climb = rows_below_cursor_in_input + 1

        if rows_to_climb > 0:
            write(f"\r{CSI}{rows_to_climb}A")
        else:
            write("\r")
        if cur_visual_col > 0:
            write(f"{CSI}{cur_visual_col}C")

        self._rendered = True
        # How many rows above the cursor is the top of the widget (top bar if
        # bordered, else first input row). Used by the next render to climb
        # back up before erasing.
        self._cursor_up_to_top = cur_visual_row_from_top + (1 if self.bordered else 0)

    def run(self) -> tuple[str, bool]:
        """Run the widget; returns (buffer, validated_by_enter)."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        prev_winch = signal.signal(
            signal.SIGWINCH, lambda *_: setattr(self, "_needs_resize", True)
        )
        validated = False
        try:
            tty.setraw(fd)
            write(KITTY_ON + MOK_ON + PASTE_ON)
            self.render()

            pending_esc = False

            while True:
                try:
                    key = read_key()
                except InterruptedError:
                    if self._needs_resize:
                        self._needs_resize = False
                        self._handle_resize()
                        self.render()
                    continue

                if self._needs_resize:
                    self._needs_resize = False
                    self._handle_resize()
                    self.render()

                if self.debug:
                    self.last_key_trace = " ".join(f"{ord(c):02x}" for c in key)

                if key == "\x1b":
                    pending_esc = True
                    continue
                if pending_esc:
                    pending_esc = False
                    if key in ("\r", "\n"):
                        self._insert("\n")
                        self.render()
                        continue
                    if key == "[":
                        key = read_csi_tail("\x1b[")
                        if self.debug:
                            self.last_key_trace = " ".join(f"{ord(c):02x}" for c in key)

                # Completion mode: hijack Up/Down/Tab/Enter for navigation
                # and acceptance, before the generic handlers see them.
                if self._in_completion_mode():
                    if key == f"{CSI}A":  # Up
                        self._completion_index = max(0, self._completion_index - 1)
                        self.render()
                        continue
                    if key == f"{CSI}B":  # Down
                        matches = self._filtered_completions()
                        if matches:
                            self._completion_index = min(
                                len(matches) - 1, self._completion_index + 1
                            )
                        self.render()
                        continue
                    if key == "\t" or key == "\r":
                        matches = self._filtered_completions()
                        if matches:
                            name = matches[self._completion_index][0]
                            self.buffer = name + " "
                            self.cursor = len(self.buffer)
                            self._completion_index = 0
                            self.render()
                            continue
                        # No matches: fall through (Enter on \r submits below).

                if key == PASTE_START:
                    pasted = read_paste().replace("\r\n", "\n").replace("\r", "\n")
                    self._insert(pasted)
                elif key == "\r":
                    if self.cursor > 0 and self.buffer[self.cursor - 1] == "\\":
                        self.buffer = (
                            self.buffer[: self.cursor - 1]
                            + "\n"
                            + self.buffer[self.cursor :]
                        )
                    else:
                        validated = True
                        self.render()
                        break
                elif key == "\x03":  # Ctrl+C
                    self.render()
                    break
                elif key in (
                    "\x1b\r",
                    "\x1b\n",
                    "\n",
                    "\x1b[13;2u",
                    "\x1b[27;2;13~",
                ):
                    self._insert("\n")
                elif key in ("\x7f", "\b"):
                    self._backspace()
                elif key == f"{CSI}D":
                    self._move(-1)
                elif key == f"{CSI}C":
                    self._move(1)
                elif key == f"{CSI}A":
                    self._move_vertical(-1)
                elif key == f"{CSI}B":
                    self._move_vertical(1)
                elif key == f"{CSI}H" or key == "\x01":
                    self._home()
                elif key == f"{CSI}F" or key == "\x05":
                    self._end()
                elif key == "\x07":  # Ctrl+G
                    self.debug = not self.debug
                elif len(key) == 1 and key.isprintable():
                    self._insert(key)
                    # Typing further in completion mode resets the selection
                    # to the first match.
                    self._completion_index = 0
                else:
                    continue

                self.render()

        finally:
            write(PASTE_OFF + MOK_OFF + KITTY_OFF)
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            signal.signal(signal.SIGWINCH, prev_winch)
            if self.bordered:
                self._erase_widget()
            else:
                # Descend below the input area using visual rows (accounting
                # for terminal wrap), so we don't bury the last visual row.
                lines = self.buffer.split("\n")
                cur_row, cur_col = cursor_rowcol(self.buffer, self.cursor)
                line_visual_rows = [self._visual_rows_for_line(l) for l in lines]
                cur_visual_offset = (self._prefix_width + cur_col) // self.width
                rows_below = (line_visual_rows[cur_row] - 1 - cur_visual_offset) + sum(
                    line_visual_rows[cur_row + 1 :]
                )
                write(f"\r{CSI}{rows_below + 1}B\r\n")

        return self.buffer, validated

    def _backspace(self) -> None:
        if self.cursor > 0:
            self.buffer = self.buffer[: self.cursor - 1] + self.buffer[self.cursor :]
            self.cursor -= 1

    def _end(self) -> None:
        nxt = self.buffer.find("\n", self.cursor)
        self.cursor = len(self.buffer) if nxt == -1 else nxt

    def _erase_widget(self) -> None:
        """Erase the rendered bordered box from the screen.

        Leaves the cursor at column 0 of the line where the top bar was, so the
        caller can print whatever representation of the submitted value it
        wants (e.g. ``❯ {value}``) into the freed space.
        """
        if self._cursor_up_to_top > 0:
            write(f"\r{CSI}{self._cursor_up_to_top}A")
        else:
            write("\r")
        write(f"{CSI}J")

    def _filtered_completions(self) -> list[tuple[str, str]]:
        """Completions whose name starts with the typed prefix (case-insensitive)."""
        if not self._in_completion_mode():
            return []
        prefix = self.buffer.lower()
        return [c for c in self.completions if c[0].lower().startswith(prefix)]

    def _handle_resize(self) -> None:
        if self._width_override is not None:
            return
        self.width = self._read_live_width()
        self._rendered = False  # force full redraw at new width

    def _home(self) -> None:
        self.cursor = self.buffer.rfind("\n", 0, self.cursor) + 1

    def _in_completion_mode(self) -> bool:
        """Completion list is active when buffer is a single token starting with /."""
        return (
            bool(self.completions)
            and self.buffer.startswith("/")
            and " " not in self.buffer
            and "\n" not in self.buffer
        )

    def _info_rows(self) -> list[str]:
        """Build the info-zone lines (either the static info or the completion list)."""
        if self._in_completion_mode():
            matches = self._filtered_completions()
            if not matches:
                return ["? (no matching command)"]
            # Clamp selection inside available matches.
            self._completion_index = max(
                0, min(self._completion_index, len(matches) - 1)
            )
            visible = matches[: self.COMPLETION_MAX_ROWS]
            name_w = max(display_width(n) for n, _ in visible)
            rows: list[str] = []
            for i, (name, desc) in enumerate(visible):
                pad = " " * max(2, 30 - name_w)  # at least 2 spaces gutter
                line_raw = f"{name}{pad}{desc}"
                # Truncate to fit terminal width (no wrap inside completion list).
                if display_width(line_raw) > self.width:
                    # Crude truncation: cut description.
                    avail = self.width - name_w - len(pad) - 1
                    if avail > 1:
                        line_raw = f"{name}{pad}{desc[: max(0, avail)]}…"
                    else:
                        line_raw = name[: self.width]
                if i == self._completion_index:
                    # Highlight selected row via reverse video.
                    rows.append(f"\x1b[7m{line_raw}\x1b[27m")
                else:
                    rows.append(line_raw)
            return rows
        # Normal info zone: a single line (may carry the debug key trace).
        info_line = self.info
        if self.debug and self.last_key_trace:
            info_line = f"{info_line}  [key={self.last_key_trace}]"
        return [f"? {info_line}"]

    def _insert(self, text: str) -> None:
        self.buffer = self.buffer[: self.cursor] + text + self.buffer[self.cursor :]
        self.cursor += len(text)

    def _move(self, delta: int) -> None:
        self.cursor = max(0, min(len(self.buffer), self.cursor + delta))

    def _move_vertical(self, delta: int) -> None:
        row, col = cursor_rowcol(self.buffer, self.cursor)
        lines = self.buffer.split("\n")
        target = row + delta
        if 0 <= target < len(lines):
            target_line = lines[target]
            offset = 0
            acc = 0
            for ch in target_line:
                w = display_width(ch)
                if acc + w > col:
                    break
                acc += w
                offset += 1
            self.cursor = sum(len(l) + 1 for l in lines[:target]) + offset

    def _read_live_width(self) -> int:
        """Ask the provider (or shutil) for the current terminal width."""
        if self._width_provider is not None:
            try:
                value = int(self._width_provider())
                if value > 0:
                    return max(20, value)
            except Exception:
                pass
        return self._terminal_width()

    def _visual_rows_for_line(self, line: str) -> int:
        """Number of visual rows a logical line occupies once the prefix is added
        and the terminal wraps at ``self.width``.
        """
        total = self._prefix_width + display_width(line)
        if total <= 0:
            return 1
        return max(1, (total + self.width - 1) // self.width)
