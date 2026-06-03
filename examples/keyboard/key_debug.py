#!/usr/bin/env python3
"""Terminal key diagnostic tool.

Prints the raw bytes emitted by each keypress in the current terminal,
hex + repr. Use this to discover which sequences your terminal produces
for keys like Shift+Enter, Alt+Enter, Ctrl+Enter, F-keys, etc.

Activates kitty keyboard protocol (CSI > 1 u) and xterm modifyOtherKeys
(CSI > 4;2 m) on entry — terminals supporting them will emit distinct
sequences for modifier+key combos. Unsupported terminals ignore these
control sequences silently.

Press Ctrl+C to quit.

Run:
    python /path/to/this/file.py
"""
from __future__ import annotations

import os
import select
import sys
import termios
import tty


ESC_TIMEOUT = 0.05  # seconds


def main() -> None:
    term = os.environ.get("TERM", "?")
    termprog = os.environ.get("TERM_PROGRAM", "?")
    print(f"TERM={term}  TERM_PROGRAM={termprog}")
    print("Press keys (Enter, Shift+Enter, Alt+Enter, Ctrl+J, arrows...).")
    print("Ctrl+C to quit.\r")

    # Try to opt into advanced keyboard protocols
    sys.stdout.write("\x1b[>1u")        # kitty keyboard protocol
    sys.stdout.write("\x1b[>4;2m")      # xterm modifyOtherKeys=2
    sys.stdout.flush()

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1)
            buf = [ch]
            # Aggregate any bytes that follow within the timeout window
            while True:
                r, _, _ = select.select([sys.stdin], [], [], ESC_TIMEOUT)
                if not r:
                    break
                buf.append(sys.stdin.read(1))
            raw = "".join(buf)
            if raw == "\x03":
                break
            hex_repr = " ".join(f"{ord(c):02x}" for c in raw)
            sys.stdout.write(
                f"len={len(raw):2d}  hex={hex_repr:30s}  repr={raw!r}\r\n"
            )
            sys.stdout.flush()
    finally:
        sys.stdout.write("\x1b[<u")        # kitty off
        sys.stdout.write("\x1b[>4;0m")     # modifyOtherKeys off
        sys.stdout.flush()
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


if __name__ == "__main__":
    main()
