#!/usr/bin/env python3
"""Single-line input widget with top/bottom bars and info zone.

Stdlib only (termios/tty/select). Demonstrates a raw-mode terminal input
without prompt_toolkit or any heavy dependency.

Layout:
    ------------------------------------------------------------
    > buffer here
    ------------------------------------------------------------
    ? info zone

Keys:
    Enter      -> validate
    Backspace  -> delete previous char
    Left/Right -> move cursor
    Home/End   -> jump start/end of line (also Ctrl+A / Ctrl+E)
    Ctrl+C     -> abort

Run:
    python /path/to/this/file.py
"""
from __future__ import annotations

import select
import shutil
import sys
import termios
import tty


CSI = "\x1b["
ESC_TIMEOUT = 0.05  # seconds to wait for escape sequence continuation


def write(s: str) -> None:
    sys.stdout.write(s)
    sys.stdout.flush()


def read_key() -> str:
    """Read one key, aggregating escape sequences with a small timeout."""
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


def render(buffer: str, cursor: int, info: str, width: int, state: dict) -> None:
    """Redraw the widget in place."""
    if state["rendered"]:
        # Go back to top of widget (input row -> bar_top is 1 line up)
        write(f"\r{CSI}1A")
        write(f"{CSI}J")  # clear from cursor to end of screen
    else:
        write("\r")

    bar = "-" * width
    write(f"{bar}\r\n")
    write(f"> {buffer}\r\n")
    write(f"{bar}\r\n")
    write(f"? {info}")

    # Reposition cursor on the input row at the right column
    write(f"\r{CSI}2A")
    if 2 + cursor > 0:
        write(f"{CSI}{2 + cursor}C")

    state["rendered"] = True


def main() -> None:
    width = min(shutil.get_terminal_size((60, 20)).columns, 60)
    buffer = ""
    cursor = 0
    info = "Enter=validate | Backspace | Left/Right | Ctrl+C=abort"
    state = {"rendered": False}

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        render(buffer, cursor, info, width, state)

        while True:
            key = read_key()

            if key == "\r":
                info = f"valeur recue: {buffer!r}"
                render(buffer, cursor, info, width, state)
                break
            if key == "\x03":  # Ctrl+C
                info = "interrompu"
                render(buffer, cursor, info, width, state)
                break

            if key in ("\x7f", "\b"):
                if cursor > 0:
                    buffer = buffer[: cursor - 1] + buffer[cursor:]
                    cursor -= 1
            elif key == f"{CSI}D":  # Left
                cursor = max(0, cursor - 1)
            elif key == f"{CSI}C":  # Right
                cursor = min(len(buffer), cursor + 1)
            elif key == f"{CSI}H" or key == "\x01":  # Home / Ctrl+A
                cursor = 0
            elif key == f"{CSI}F" or key == "\x05":  # End / Ctrl+E
                cursor = len(buffer)
            elif len(key) == 1 and key.isprintable() and len(buffer) < width - 4:
                buffer = buffer[:cursor] + key + buffer[cursor:]
                cursor += 1
            else:
                continue

            info = f"len={len(buffer)} cursor={cursor}"
            render(buffer, cursor, info, width, state)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        write(f"{CSI}2B\r\n")


if __name__ == "__main__":
    main()
