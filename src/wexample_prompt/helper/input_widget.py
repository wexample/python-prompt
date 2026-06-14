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

import os
import select
import shutil
import signal
import sys
import termios
import tty

from wcwidth import wcswidth

CSI = "\x1b["

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
        resize_subscribe=None,
    ) -> None:
        # An explicit `width` kwarg fixes the widget at that size and disables
        # resize handling. `width_provider` is the "live" source — called on
        # init and on SIGWINCH; if provided it wins over the static fallback.
        self._width_override = width
        self._width_provider = width_provider
        # `resize_subscribe(callback) -> unsubscribe_fn`: hook into a shared
        # SIGWINCH dispatcher (typically IoManager.subscribe_resize). When
        # provided, the widget skips installing its own SIGWINCH handler —
        # avoids fighting with whoever owns the signal globally.
        self._resize_subscribe = resize_subscribe
        self.width = width or self._read_live_width()
        self.info = info
        self.debug = debug
        # Debug overlay: rolling window of the last N raw bytes received
        # from stdin, with their inter-byte gap (ms). One entry per byte —
        # NOT per logical key — so the overlay refreshes the instant a
        # byte hits the widget, even if the surrounding escape sequence
        # is incomplete. Bypasses any reconstruction logic. Toggled by
        # `debug=True` at init or Ctrl+G at runtime.
        self._debug_history: list[tuple[float, str, float]] = []
        self.DEBUG_HISTORY_SIZE = 16
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
        self._bar = BAR_CHAR * self.width

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
            write(f"{self._bar}\r\n")

        for i, line in enumerate(lines):
            prefix = self.prompt_prefix if i == 0 else self.continuation_prefix
            write(f"{prefix}{line}\r\n")

        info_rows: list[str] = []
        if self.bordered:
            write(f"{self._bar}\r\n")
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
        # Resize wiring — prefer the shared subscriber (single SIGWINCH
        # handler at IoManager level); fall back to a local handler when
        # the widget is used standalone (demo scripts, tests).
        _on_resize = lambda: setattr(self, "_needs_resize", True)  # noqa: E731
        if self._resize_subscribe is not None:
            unsubscribe_resize = self._resize_subscribe(_on_resize)
            prev_winch = None
        else:
            unsubscribe_resize = None
            prev_winch = signal.signal(signal.SIGWINCH, lambda *_: _on_resize())
        validated = False
        try:
            tty.setraw(fd)
            write(KITTY_ON + MOK_ON + PASTE_ON)
            self.render()

            # Reading is fully decoupled from key parsing:
            #   - `drain_stdin_nonblocking` reads bytes as they come, in
            #     bursts, and records each one for the optional debug
            #     overlay.
            #   - `_try_extract_key` is a pure function over the byte
            #     buffer: it returns one complete key at a time (plain
            #     char / Alt+X / CSI / SS3 / bracketed paste) or None if
            #     more bytes are needed. Easy to unit-test on its own.

            import time as _t

            # A bare ESC press has no action in this widget, so we don't
            # need to disambiguate it quickly. The budget exists only to
            # eventually drop an ESC that never completes — keeping it
            # generous costs nothing.
            ESC_SEQ_BUDGET = 0.5
            POLL_SLICE = 0.05  # idle pause between non-blocking checks

            buffer = ""
            esc_seq_started_at: float | None = None
            last_byte_at: float | None = None

            def _record_byte(c: str) -> None:
                """Log one freshly-read byte and refresh the overlay."""
                nonlocal last_byte_at
                now = _t.monotonic()
                waited_ms = (
                    ((now - last_byte_at) * 1000.0) if last_byte_at is not None else 0.0
                )
                last_byte_at = now
                if not self.debug:
                    return
                self._debug_history.append((now, c, waited_ms))
                if len(self._debug_history) > self.DEBUG_HISTORY_SIZE:
                    self._debug_history = self._debug_history[
                        -self.DEBUG_HISTORY_SIZE :
                    ]
                # Render right away so the user sees the byte instantly,
                # without waiting for the rest of its sequence to arrive.
                self.render()

            def drain_stdin_nonblocking() -> None:
                """Pull every available byte from the tty in one syscall.

                Uses `os.read(fd, N)` rather than `sys.stdin.read(1)` to
                bypass Python's TextIO buffer — otherwise `select()` goes
                blind to bytes already pulled into that buffer, and the
                tail of an escape sequence stays invisible until the next
                keystroke triggers another syscall.
                """
                nonlocal buffer, esc_seq_started_at
                while True:
                    try:
                        r, _, _ = select.select([fd], [], [], 0)
                    except InterruptedError:
                        break
                    if not r:
                        break
                    chunk_bytes = os.read(fd, 1024)
                    if not chunk_bytes:
                        break
                    chunk = chunk_bytes.decode("utf-8", errors="replace")
                    for c in chunk:
                        _record_byte(c)
                        if c == "\x1b" and esc_seq_started_at is None:
                            esc_seq_started_at = _t.monotonic()
                    buffer += chunk

            while True:
                if self._needs_resize:
                    self._needs_resize = False
                    self._handle_resize()
                    self.render()

                drain_stdin_nonblocking()

                key, consumed = self._try_extract_key(
                    buffer, esc_seq_started_at, _t.monotonic(), ESC_SEQ_BUDGET
                )

                if key is None:
                    # Need more bytes — wait briefly for them. Use the
                    # raw fd (not sys.stdin) for the same reason as the
                    # drain loop: avoid Python's TextIO buffer making
                    # select() blind to bytes that have already arrived.
                    try:
                        select.select([fd], [], [], POLL_SLICE)
                    except InterruptedError:
                        pass
                    continue

                # Consume the bytes that made up this key.
                buffer = buffer[consumed:]
                if not buffer.startswith("\x1b"):
                    esc_seq_started_at = None

                # Special: bare-ESC sequence that timed out — drop silently.
                if key == "__DROP__":
                    continue

                # Bracketed paste comes pre-extracted as a tuple from the
                # state machine, before the str-only handlers below.
                if isinstance(key, tuple) and key and key[0] == "PASTE":
                    pasted = key[1].replace("\r\n", "\n").replace("\r", "\n")
                    self._insert(pasted)
                    self.render()
                    continue

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

                if key == "\r":
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
            if unsubscribe_resize is not None:
                unsubscribe_resize()
            elif prev_winch is not None:
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
        # Wipe the old widget BEFORE re-measuring. Without this, render()
        # would take the `_rendered=False` branch (no erase, just `\r`) and
        # paint the new geometry below the stale one — each resize would
        # stack a new top bar onto the previous render.
        #
        # We climb exactly `_cursor_up_to_top` rows (the count measured at
        # the OLD width) and erase to end of screen. In terminals that
        # reflow already-drawn lines on resize (gnome-terminal, kitty,
        # iTerm2) a narrower window may leave a single row of stale top
        # bar above — visible but harmless. We deliberately don't
        # over-climb to compensate: non-reflowing terminals (xterm) would
        # then erase the user's scrollback above us, which is much worse.
        if self._rendered:
            if self._cursor_up_to_top > 0:
                write(f"\r{CSI}{self._cursor_up_to_top}A")
            else:
                write("\r")
            write(f"{CSI}J")
        self.width = self._read_live_width()
        self._bar = BAR_CHAR * self.width
        self._rendered = False  # next render() paints fresh, no climb

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
        rows: list[str] = []
        if self._in_completion_mode():
            matches = self._filtered_completions()
            if not matches:
                rows = ["? (no matching command)"]
            else:
                # Clamp selection inside available matches.
                self._completion_index = max(
                    0, min(self._completion_index, len(matches) - 1)
                )
                visible = matches[: self.COMPLETION_MAX_ROWS]
                name_w = max(display_width(n) for n, _ in visible)
                pad = " " * max(2, 30 - name_w)  # at least 2 spaces gutter
                for i, (name, desc) in enumerate(visible):
                    line_raw = f"{name}{pad}{desc}"
                    # Truncate to fit terminal width (no wrap inside completion list).
                    if display_width(line_raw) > self.width:
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
        else:
            # Normal info zone: a single line.
            rows = [f"? {self.info}"]

        # Debug overlay — one row per raw byte received from stdin, in
        # arrival order, with the gap (ms) since the previous byte. This
        # is intentionally a flat byte log: NO reconstruction, NO key
        # aggregation. If `\x1b` arrives now and `[B` only 3s later, you
        # see them as three separate lines with their real timing — which
        # is what we need to debug the terminal/tty fragmentation.
        if self.debug and self._debug_history:
            rows.append(f"── debug (last {len(self._debug_history)} bytes) ──")
            for _ts, b, waited_ms in self._debug_history:
                rows.append(f"  +{waited_ms:6.0f} ms   0x{ord(b):02x}   {b!r}")
        return rows

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
            _dw = display_width
            for ch in target_line:
                w = _dw(ch)
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

    def _try_extract_key(
        self,
        buf: str,
        esc_seq_started_at: float | None,
        now: float,
        budget: float,
    ):
        """Parse the head of `buf` into one complete key.

        Returns a tuple (key, consumed) where `consumed` is the number of
        bytes to drop from the buffer. Returns (None, 0) when the buffer
        is incomplete and we should wait for more bytes.

        Special return: `("__DROP__", n)` means "consume n bytes silently"
        — used when an ESC sequence didn't complete within the budget.
        """
        if not buf:
            return None, 0

        # Plain char (no escape prefix).
        if buf[0] != "\x1b":
            return buf[0], 1

        # Bracketed paste: the most reliable bracketed CSI we know — read
        # straight through to the end marker before dispatching.
        if buf.startswith(PASTE_START):
            end_idx = buf.find(PASTE_END, len(PASTE_START))
            if end_idx == -1:
                # Incomplete — wait. (No timeout for paste: we trust the
                # terminal to deliver the closing marker eventually.)
                return None, 0
            text = buf[len(PASTE_START) : end_idx]
            return ("PASTE", text), end_idx + len(PASTE_END)

        # Need at least 2 bytes to decide what kind of ESC sequence.
        timed_out = (
            esc_seq_started_at is not None and (now - esc_seq_started_at) >= budget
        )
        if len(buf) < 2:
            # Bare ESC: wait for more, drop silently after budget.
            if timed_out:
                return "__DROP__", 1
            return None, 0

        c2 = buf[1]
        if c2 not in "[O":
            # Alt+<c2>: 2-byte sequence (Alt+Enter, Alt+letter, etc.).
            return buf[:2], 2

        # CSI (\x1b[) or SS3 (\x1bO): scan for the final byte (0x40..0x7E).
        for i in range(2, len(buf)):
            c = buf[i]
            if "\x40" <= c <= "\x7e":
                return buf[: i + 1], i + 1

        # Incomplete CSI/SS3.
        if timed_out:
            # Drop the whole partial sequence — including the buffered
            # bytes — to avoid them re-emerging as literal chars.
            return "__DROP__", len(buf)
        return None, 0

    def _visual_rows_for_line(self, line: str) -> int:
        """Number of visual rows a logical line occupies once the prefix is added
        and the terminal wraps at ``self.width``.
        """
        total = self._prefix_width + display_width(line)
        if total <= 0:
            return 1
        return max(1, (total + self.width - 1) // self.width)
