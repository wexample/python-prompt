#!/usr/bin/env python3
"""Multiline input widget with newline support, stdlib only.

Layout:
    ------------------------------------------------------------
    > first line
    . second line
    . third line
    ------------------------------------------------------------
    ? info zone

Keys:
    Enter                            -> submit
    Shift+Enter / Alt+Enter / Ctrl+J -> insert newline
    Backslash (\\) + Enter            -> insert newline (Claude-style)
    Backspace                        -> delete previous char (crosses newlines)
    Left / Right                     -> move cursor
    Up / Down                        -> move cursor across lines
    Home / End (or Ctrl+A / Ctrl+E)  -> jump to line start/end
    Ctrl+G                           -> toggle key-trace overlay
    Ctrl+C                           -> abort

Bracketed paste (CSI ?2004h) is enabled, so multiline pastes are inserted
as-is including their internal newlines.

Run:
    python /path/to/this/file.py
    python /path/to/this/file.py --debug    # start with key-trace overlay on
"""
from __future__ import annotations

import select
import shutil
import sys
import termios
import tty


CSI = "\x1b["
ESC_TIMEOUT = 0.05  # seconds — long enough to catch Alt/Shift+Enter as one event

KITTY_ON = "\x1b[>1u"
KITTY_OFF = "\x1b[<u"
MOK_ON = "\x1b[>4;2m"          # xterm modifyOtherKeys=2
MOK_OFF = "\x1b[>4;0m"
PASTE_ON = "\x1b[?2004h"
PASTE_OFF = "\x1b[?2004l"
PASTE_START = "\x1b[200~"
PASTE_END = "\x1b[201~"


def write(s: str) -> None:
    sys.stdout.write(s)
    sys.stdout.flush()


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
    while True:
        ch = sys.stdin.read(1)
        buf.append(ch)
        tail = "".join(buf[-len(PASTE_END):])
        if tail == PASTE_END:
            return "".join(buf[: -len(PASTE_END)])


def cursor_rowcol(buffer: str, cursor: int) -> tuple[int, int]:
    before = buffer[:cursor]
    row = before.count("\n")
    last_nl = before.rfind("\n")
    col = len(before) if last_nl == -1 else len(before) - last_nl - 1
    return row, col


class InputWidget:
    """Reusable multi-line input widget rendered in raw terminal mode."""

    def __init__(
        self,
        width: int | None = None,
        info: str = "Enter=submit | Shift+Enter / Alt+Enter / Ctrl+J=newline | Ctrl+G=debug | Ctrl+C=abort",
        debug: bool = False,
        initial: str = "",
    ) -> None:
        term_cols = shutil.get_terminal_size((60, 20)).columns
        self.width = width or min(term_cols, 80)
        self.default_info = info
        self.info = info
        self.debug = debug
        self.last_key_trace = ""
        self.buffer = initial
        self.cursor = len(initial)
        self._state = {"rendered": False, "cursor_up_to_top": 0}

    # ---------- rendering ----------

    def render(self) -> None:
        lines = self.buffer.split("\n")
        cur_row, cur_col = cursor_rowcol(self.buffer, self.cursor)

        if self._state["rendered"]:
            up = self._state["cursor_up_to_top"]
            if up > 0:
                write(f"\r{CSI}{up}A")
            else:
                write("\r")
            write(f"{CSI}J")
        else:
            write("\r")

        bar = "-" * self.width
        write(f"{bar}\r\n")
        for i, line in enumerate(lines):
            prefix = "> " if i == 0 else ". "
            write(f"{prefix}{line}\r\n")
        write(f"{bar}\r\n")

        info_line = self.info
        if self.debug and self.last_key_trace:
            info_line = f"{info_line}  [key={self.last_key_trace}]"
        write(f"? {info_line}")

        up_to_input = len(lines) + 1 - cur_row
        write(f"\r{CSI}{up_to_input}A")
        if 2 + cur_col > 0:
            write(f"{CSI}{2 + cur_col}C")

        self._state["rendered"] = True
        self._state["cursor_up_to_top"] = 1 + cur_row

    # ---------- mutations ----------

    def _insert(self, text: str) -> None:
        self.buffer = self.buffer[: self.cursor] + text + self.buffer[self.cursor :]
        self.cursor += len(text)

    def _backspace(self) -> None:
        if self.cursor > 0:
            self.buffer = self.buffer[: self.cursor - 1] + self.buffer[self.cursor :]
            self.cursor -= 1

    def _move(self, delta: int) -> None:
        self.cursor = max(0, min(len(self.buffer), self.cursor + delta))

    def _home(self) -> None:
        self.cursor = self.buffer.rfind("\n", 0, self.cursor) + 1

    def _end(self) -> None:
        nxt = self.buffer.find("\n", self.cursor)
        self.cursor = len(self.buffer) if nxt == -1 else nxt

    def _move_vertical(self, delta: int) -> None:
        row, col = cursor_rowcol(self.buffer, self.cursor)
        lines = self.buffer.split("\n")
        target = row + delta
        if 0 <= target < len(lines):
            target_col = min(col, len(lines[target]))
            self.cursor = sum(len(l) + 1 for l in lines[:target]) + target_col

    # ---------- main loop ----------

    def run(self) -> tuple[str, bool]:
        """Run the widget; returns (buffer, validated_by_enter)."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        validated = False
        try:
            tty.setraw(fd)
            write(KITTY_ON + MOK_ON + PASTE_ON)
            self.render()

            while True:
                key = read_key()
                if self.debug:
                    self.last_key_trace = " ".join(f"{ord(c):02x}" for c in key)

                if key == PASTE_START:
                    pasted = read_paste()
                    # Normalize CR/CRLF inside paste to \n
                    pasted = pasted.replace("\r\n", "\n").replace("\r", "\n")
                    self._insert(pasted)
                elif key == "\r":
                    # Backslash + Enter = continuation (Claude-style)
                    if self.cursor > 0 and self.buffer[self.cursor - 1] == "\\":
                        self.buffer = self.buffer[: self.cursor - 1] + "\n" + self.buffer[self.cursor :]
                        # cursor stays at same numeric index, which is now after the \n
                    else:
                        validated = True
                        self.info = (
                            f"submitted ({self.buffer.count(chr(10)) + 1} lines, "
                            f"{len(self.buffer)} chars)"
                        )
                        self.render()
                        break
                elif key == "\x03":  # Ctrl+C
                    self.info = "aborted"
                    self.render()
                    break
                elif key in ("\x1b\r", "\x1b\n", "\n", "\x1b[13;2u", "\x1b[27;2;13~"):
                    # Shift+Enter, Alt+Enter, Ctrl+J, kitty form, modifyOtherKeys form
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
                    continue  # unhandled key: no re-render

                if not self.debug:
                    row, col = cursor_rowcol(self.buffer, self.cursor)
                    self.info = (
                        f"{self.default_info}  [row={row} col={col} len={len(self.buffer)}]"
                    )
                self.render()

        finally:
            write(PASTE_OFF + MOK_OFF + KITTY_OFF)
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            # Move cursor below widget so subsequent output doesn't overlap
            row, _ = cursor_rowcol(self.buffer, self.cursor)
            total_lines = self.buffer.count("\n") + 1
            below = (total_lines - row) + 1
            write(f"\r{CSI}{below}B\r\n")

        return self.buffer, validated


def main() -> None:
    debug = "--debug" in sys.argv[1:]
    widget = InputWidget(debug=debug)
    value, ok = widget.run()
    status = "SUBMITTED" if ok else "ABORTED"
    print(f"[{status}] {value!r}")


if __name__ == "__main__":
    main()
