from __future__ import annotations


class WithIndentation:
    _indent_string: str = "  "
    _indentation: int = 0

    def indentation_up(self, number: int = 1) -> None:
        self._indentation += number

    def indentation_down(self, number: int = 1) -> None:
        self._indentation -= number

    @property
    def indentation(self) -> int:
        return self._indentation
