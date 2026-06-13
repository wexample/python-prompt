#!/usr/bin/env python3
"""Measure inter-byte lag of escape sequences on your terminal.

Run::

    python measure_lag.py

Then press various keys (arrows, Shift+Enter, Alt+Enter, paste a block, …) for
~10 seconds. Ctrl+C to stop. The script reports the min / median / max / p99
gap between consecutive bytes of a same escape sequence, and suggests a safe
``ESC_TIMEOUT`` for ``input_widget.py``.

What we measure
---------------
After each ``\\x1b`` (ESC) byte, we keep reading bytes and record the time
elapsed since the previous byte. Sequences are considered finished when:
  - 250 ms pass with no new byte (safety cap), or
  - a CSI final byte (0x40..0x7e) is read after ``\\x1b[``, or
  - the second byte isn't ``[`` or ``O`` (SS3) — bare ESC or Alt+key.

Only the within-sequence gaps are collected.
"""

from __future__ import annotations

import select
import statistics
import sys
import termios
import time
import tty


CAP = 0.250  # safety cap for sequence boundary detection


def main() -> None:
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    gaps_ms: list[float] = []
    sequences: int = 0

    print("Press keys to measure (arrows, Shift+Enter, paste…). Ctrl+C to stop.\n")
    try:
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1)
            if ch == "\x03":  # Ctrl+C
                break
            if ch != "\x1b":
                continue
            # Enter sequence: read tail while bytes keep coming under CAP.
            sequences += 1
            last = time.monotonic()
            tail: list[str] = ["\x1b"]
            while True:
                r, _, _ = select.select([sys.stdin], [], [], CAP)
                if not r:
                    break
                c = sys.stdin.read(1)
                now = time.monotonic()
                gap_ms = (now - last) * 1000.0
                gaps_ms.append(gap_ms)
                tail.append(c)
                last = now
                # Stop heuristics matching input_widget.read_key()
                if len(tail) >= 3 and tail[1] == "[" and 0x40 <= ord(c) <= 0x7E:
                    break
                if len(tail) == 2 and tail[1] not in "[O":
                    break
    except KeyboardInterrupt:
        pass
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

    print()
    if not gaps_ms:
        print("No escape sequences observed.")
        return

    gaps_ms.sort()
    p50 = statistics.median(gaps_ms)
    p99 = gaps_ms[max(0, int(len(gaps_ms) * 0.99) - 1)]
    suggested_ms = max(20.0, p99 * 2.0)  # 2× p99, floor 20ms

    print(f"Sequences observed : {sequences}")
    print(f"Inter-byte samples : {len(gaps_ms)}")
    print(f"min                : {gaps_ms[0]:.1f} ms")
    print(f"median (p50)       : {p50:.1f} ms")
    print(f"p99                : {p99:.1f} ms")
    print(f"max                : {gaps_ms[-1]:.1f} ms")
    print()
    print(f"Suggested ESC_TIMEOUT : {suggested_ms / 1000:.3f} s ({suggested_ms:.0f} ms)")
    print("(2× observed p99, never below 20 ms)")


if __name__ == "__main__":
    main()
