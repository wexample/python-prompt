#!/usr/bin/env python3
"""Standalone demo of the input widget.

Run::

    python input_widget.py [--debug] [--no-border]
"""

from __future__ import annotations

import sys

from wexample_prompt.helper.input_widget import InputWidget


def main() -> None:
    args = sys.argv[1:]
    widget = InputWidget(
        debug="--debug" in args,
        bordered="--no-border" not in args,
    )
    value, ok = widget.run()
    print(f"[{'SUBMITTED' if ok else 'ABORTED'}] {value!r}")


if __name__ == "__main__":
    main()
