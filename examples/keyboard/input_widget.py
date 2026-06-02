#!/usr/bin/env python3
"""Multiline input widget rendered in raw terminal mode, stdlib only.

Layout:
    ────────────────────────────────────────
    > first line
    . second line
    ────────────────────────────────────────
    ? info zone

Keys:
    Enter                            -> submit
    Shift+Enter / Alt+Enter / Ctrl+J -> insert newline
    Backslash + Enter                -> insert newline (Claude-style)
    Backspace                        -> delete previous char
    Left / Right                     -> move cursor
    Up / Down                        -> move across lines
    Home / End (or Ctrl+A / Ctrl+E)  -> jump to line start/end
    Ctrl+G                           -> toggle key-trace overlay
    Ctrl+C                           -> abort

Bracketed paste is enabled, so multiline pastes are inserted as a block.

Run:
    python input_widget.py
    python input_widget.py --debug
"""
from __future__ import annotations

import select
import shutil
import sys
import termios
import tty


CSI = "\x1b["
ESC_TIMEOUT = 0.2  # max gap between escape-sequence bytes

KITTY_ON = "\x1b[>1u"
KITTY_OFF = "\x1b[<u"
MOK_ON = "\x1b[>4;2m"          # xterm modifyOtherKeys=2
MOK_OFF = "\x1b[>4;0m"
PASTE_ON = "\x1b[?2004h"
PASTE_OFF = "\x1b[?2004l"
PASTE_START = "\x1b[200~"
PASTE_END = "\x1b[201~"

BAR_CHAR = "─"  # ─ U+2500 BOX DRAWINGS LIGHT HORIZONTAL

DEFAULT_INFO = "Enter=submit | Shift+Enter=newline | Ctrl+G=debug | Ctrl+C=abort"


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
    end_len = len(PASTE_END)
    while True:
        buf.append(sys.stdin.read(1))
        if "".join(buf[-end_len:]) == PASTE_END:
            return "".join(buf[:-end_len])


def cursor_rowcol(buffer: str, cursor: int) -> tuple[int, int]:
    before = buffer[:cursor]
    row = before.count("\n")
    last_nl = before.rfind("\n")
    col = len(before) if last_nl == -1 else len(before) - last_nl - 1
    return row, col


class InputWidget:
    """Reusable multi-line input widget."""

    def __init__(
        self,
        width: int | None = None,
        info: str = DEFAULT_INFO,
        debug: bool = False,
        initial: str = "",
    ) -> None:
        term_cols = shutil.get_terminal_size((60, 20)).columns
        self.width = width or min(term_cols, 80)
        self.info = info
        self.debug = debug
        self.last_key_trace = ""
        self.buffer = initial
        self.cursor = len(initial)
        self._rendered = False
        self._cursor_up_to_top = 0

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

        bar = BAR_CHAR * self.width
        write(f"{bar}\r\n")
        for i, line in enumerate(lines):
            prefix = "> " if i == 0 else ". "
            write(f"{prefix}{line}\r\n")
        write(f"{bar}\r\n")

        info_line = self.info
        if self.debug and self.last_key_trace:
            info_line = f"{info_line}  [key={self.last_key_trace}]"
        write(f"? {info_line}")

        write(f"\r{CSI}{len(lines) + 1 - cur_row}A")
        if 2 + cur_col > 0:
            write(f"{CSI}{2 + cur_col}C")

        self._rendered = True
        self._cursor_up_to_top = 1 + cur_row

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
            target_col = min(col, len(lines[target]))
            self.cursor = sum(len(l) + 1 for l in lines[:target]) + target_col

    def _home(self) -> None:
        self.cursor = self.buffer.rfind("\n", 0, self.cursor) + 1

    def _end(self) -> None:
        nxt = self.buffer.find("\n", self.cursor)
        self.cursor = len(self.buffer) if nxt == -1 else nxt

    def run(self) -> tuple[str, bool]:
        """Run the widget; returns (buffer, validated_by_enter)."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        validated = False
        try:
            tty.setraw(fd)
            write(KITTY_ON + MOK_ON + PASTE_ON)
            self.render()

            # gnome-terminal sends \x1b then \r far apart for Shift+Enter / Alt+Enter,
            # past the ESC_TIMEOUT window — track a pending ESC across iterations.
            pending_esc = False

            while True:
                key = read_key()
                if self.debug:
                    self.last_key_trace = " ".join(f"{ord(c):02x}" for c in key)

                if key == "\x1b":
                    pending_esc = True
                    continue
                if pending_esc and key in ("\r", "\n"):
                    pending_esc = False
                    self._insert("\n")
                    self.render()
                    continue
                pending_esc = False

                if key == PASTE_START:
                    pasted = read_paste().replace("\r\n", "\n").replace("\r", "\n")
                    self._insert(pasted)
                elif key == "\r":
                    if self.cursor > 0 and self.buffer[self.cursor - 1] == "\\":
                        # backslash + Enter -> line continuation
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
                elif key in ("\x1b\r", "\x1b\n", "\n", "\x1b[13;2u", "\x1b[27;2;13~"):
                    # aggregated Shift+Enter / Alt+Enter (fast terminals), Ctrl+J, kitty, MOK
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
                    continue  # unknown sequence: no re-render

                self.render()

        finally:
            write(PASTE_OFF + MOK_OFF + KITTY_OFF)
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            row, _ = cursor_rowcol(self.buffer, self.cursor)
            total = self.buffer.count("\n") + 1
            write(f"\r{CSI}{(total - row) + 1}B\r\n")

        return self.buffer, validated


def main() -> None:
    widget = InputWidget(debug="--debug" in sys.argv[1:])
    value, ok = widget.run()
    print(f"[{'SUBMITTED' if ok else 'ABORTED'}] {value!r}")


if __name__ == "__main__":
    main()
