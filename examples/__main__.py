from __future__ import annotations

import sys

from wexample_helpers.classes.example.executor import Executor


def _parse_filters(argv: list[str]) -> tuple[str, ...] | None:
    cleaned = tuple(arg.strip() for arg in argv if arg.strip())
    return cleaned or None

if __name__ == "__main__":
    filters = _parse_filters(sys.argv[1:])
    Executor(
        entrypoint_path=__file__,
        filters=filters,
    ).execute()
