#!/usr/bin/env python3
"""Terminal key diagnostic tool.

Prints each raw byte received from the terminal, with:
  - the byte (hex + repr)
  - the time gap since the previous byte (milliseconds)
  - a blank line every time the gap exceeds 100ms (= probable end of a
    keystroke / escape sequence)

This is the right tool for diagnosing arrow-key bugs in input_widget.py:
if your terminal delivers `\\x1b` … (>200ms gap) … `[B`, the widget can't
tell `Down` from a real Escape press unless its CSI tail timeout is
generous enough.

Activates kitty keyboard protocol (CSI > 1 u) and xterm modifyOtherKeys
(CSI > 4;2 m) on entry — terminals supporting them emit distinct
sequences for modifier+key combos. Unsupported terminals ignore them.

Press Ctrl+C to quit.

Run:
    python /path/to/this/file.py
"""
from __future__ import annotations

import os
import sys
import termios
import time
import tty


GAP_FLUSH_MS = 100  # blank line when the gap between bytes exceeds this


def main() -> None:
    term = os.environ.get("TERM", "?")
    termprog = os.environ.get("TERM_PROGRAM", "?")
    print(f"TERM={term}  TERM_PROGRAM={termprog}")
    print(
        "Each row = one byte. Press keys and watch the inter-byte gap "
        "(ms). Blank line ≈ end of a keystroke."
    )
    print("Ctrl+C to quit.\r")

    # Opt into advanced keyboard protocols.
    sys.stdout.write("\x1b[>1u")     # kitty keyboard protocol
    sys.stdout.write("\x1b[>4;2m")   # xterm modifyOtherKeys=2
    sys.stdout.flush()

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    last_t: float | None = None
    try:
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1)
            now = time.monotonic()
            gap_ms = (now - last_t) * 1000.0 if last_t is not None else 0.0
            last_t = now
            if gap_ms >= GAP_FLUSH_MS:
                sys.stdout.write("\r\n")
            if ch == "\x03":
                sys.stdout.write("(Ctrl+C — quit)\r\n")
                break
            sys.stdout.write(
                f"  gap={gap_ms:6.1f} ms   byte=0x{ord(ch):02x}   repr={ch!r}\r\n"
            )
            sys.stdout.flush()
    finally:
        sys.stdout.write("\x1b[<u")
        sys.stdout.write("\x1b[>4;0m")
        sys.stdout.flush()
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


if __name__ == "__main__":
    main()
