from __future__ import annotations

from wexample_helpers.decorator.base_class import base_class


@base_class
class WithIndentation:
    _indent_string: str = "  "
    _indentation: int = 0

    @property
    def indentation(self) -> int:
        return self._indentation

    def indentation_down(self, number: int = 1) -> None:
        self._indentation -= number

    def indentation_up(self, number: int = 1) -> None:
        self._indentation += number
