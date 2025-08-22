"""Abstract base class for interactive prompt responses."""
from __future__ import annotations

from abc import ABC
from typing import Any

from pydantic import Field
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse


class AbstractInteractivePromptResponse(AbstractPromptResponse, ABC):
    """Base for interactive responses with common terminal helpers."""

    reset_on_finish: bool = Field(
        default=False,
        description="If True, clears the prompt block from the terminal after a selection or abort.",
    )
    _answer: Any = None

    @staticmethod
    def _partial_clear(printed_lines: int) -> None:
        if printed_lines > 0:
            print(f"\033[{printed_lines}F\033[J", end="")

    def _print_render(self, context) -> int:
        rendered = super().render(context=context)
        if rendered is None:
            return 0
        print(rendered)
        return rendered.count("\n") + 1

    @staticmethod
    def _read_key() -> str:
        import readchar

        return readchar.readkey()

    def get_answer(self) -> Any:
        return self._answer
