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
ESC_TIMEOUT = 0.2  # max gap between escape-sequence bytes

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


def write(s: str) -> None:
    sys.stdout.write(s)
    sys.stdout.flush()


def display_width(s: str) -> int:
    """Width in terminal columns, treating wide chars (emoji/CJK) as 2."""
    w = wcswidth(s)
    return w if w >= 0 else len(s)


def read_csi_tail(prefix: str = "\x1b[") -> str:
    """Read remaining bytes of a CSI sequence until its final byte."""
    seq = prefix
    while True:
        r, _, _ = select.select([sys.stdin], [], [], ESC_TIMEOUT)
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
    seq = "\x1b"
    while True:
        r, _, _ = select.select([sys.stdin], [], [], ESC_TIMEOUT)
        if not r:
            break
        c = sys.stdin.read(1)
        seq += c
        if len(seq) >= 3 and seq[1] == "[" and 0x40 <= ord(c) <= 0x7E:
            break
        if len(seq) == 2 and seq[1] not in "[O":
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


def cursor_rowcol(buffer: str, cursor: int) -> tuple[int, int]:
    before = buffer[:cursor]
    row = before.count("\n")
    last_nl = before.rfind("\n")
    line_before = before if last_nl == -1 else before[last_nl + 1 :]
    return row, display_width(line_before)


class InputWidget:
    """Reusable multi-line input widget rendered inline (no full-screen)."""

    def __init__(
        self,
        width: int | None = None,
        info: str = DEFAULT_INFO,
        debug: bool = False,
        initial: str = "",
        bordered: bool = True,
        prompt_prefix: str = "> ",
        continuation_prefix: str | None = None,
    ) -> None:
        self._width_override = width
        self.width = width or self._terminal_width()
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
        self._rendered = False
        self._cursor_up_to_top = 0
        self._needs_resize = False

    @staticmethod
    def _terminal_width() -> int:
        return min(shutil.get_terminal_size((60, 20)).columns, 80)

    def render(self) -> None:
        lines = self.buffer.split("\n")
        cur_row, cur_col = cursor_rowcol(self.buffer, self.cursor)

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

        if self.bordered:
            write(f"{BAR_CHAR * self.width}\r\n")
            info_line = self.info
            if self.debug and self.last_key_trace:
                info_line = f"{info_line}  [key={self.last_key_trace}]"
            write(f"? {info_line}")

        # Position cursor on the input line at the right column.
        rows_below_input_top = len(lines) - cur_row
        rows_to_climb = rows_below_input_top
        if self.bordered:
            rows_to_climb += 1  # bottom bar
        write(f"\r{CSI}{rows_to_climb}A")
        if self._prefix_width + cur_col > 0:
            write(f"{CSI}{self._prefix_width + cur_col}C")

        self._rendered = True
        # How many rows above us is the top of the widget (top bar if bordered,
        # else first input line). Used by the next render to climb back up.
        self._cursor_up_to_top = cur_row + (1 if self.bordered else 0)

    def _insert(self, text: str) -> None:
        self.buffer = self.buffer[: self.cursor] + text + self.buffer[self.cursor :]
        self.cursor += len(text)

    def _backspace(self) -> None:
        if self.cursor > 0:
            self.buffer = self.buffer[: self.cursor - 1] + self.buffer[self.cursor :]
            self.cursor -= 1

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

    def _home(self) -> None:
        self.cursor = self.buffer.rfind("\n", 0, self.cursor) + 1

    def _end(self) -> None:
        nxt = self.buffer.find("\n", self.cursor)
        self.cursor = len(self.buffer) if nxt == -1 else nxt

    def _handle_resize(self) -> None:
        if self._width_override is not None:
            return
        self.width = self._terminal_width()
        self._rendered = False  # force full redraw at new width

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
                            self.last_key_trace = " ".join(
                                f"{ord(c):02x}" for c in key
                            )

                if key == PASTE_START:
                    pasted = (
                        read_paste().replace("\r\n", "\n").replace("\r", "\n")
                    )
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
                row, _ = cursor_rowcol(self.buffer, self.cursor)
                total = self.buffer.count("\n") + 1
                rows_below = total - row
                write(f"\r{CSI}{rows_below}B\r\n")

        return self.buffer, validated

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
