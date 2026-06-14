"""Free-text input interactive response."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.const.types import LineMessage
from wexample_prompt.responses.interactive.abstract_interactive_prompt_response import (
    AbstractInteractivePromptResponse,
)

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext


@base_class
class InputPromptResponse(AbstractInteractivePromptResponse):
    """Prompt the user for a free-text value.

    Displays a styled question line then reads a full line of text from stdin.
    Supports ``predefined_answer`` for non-interactive (testing) contexts.
    """

    default_value: str | None = public_field(
        default=None,
        description="Pre-filled value shown in brackets; accepted when the user presses Enter on an empty line",
    )
    predefined_answer: Any = public_field(
        default=None,
        description="Skip stdin and return this value directly (non-interactive / testing)",
    )
    question: LineMessage = public_field(
        default="Enter a value:",
        description="Question shown before the input cursor",
    )

    @classmethod
    def create_input(
        cls,
        question: LineMessage = "Enter a value:",
        default_value: str | None = None,
        predefined_answer: Any = None,
        reset_on_finish: bool = False,
    ) -> InputPromptResponse:
        return cls(
            question=question,
            default_value=default_value,
            predefined_answer=predefined_answer,
            reset_on_finish=reset_on_finish,
        )

    @classmethod
    def get_example_class(cls) -> type:
        from wexample_prompt.example.response.interactive.input_example import (
            InputExample,
        )

        return InputExample

    def get_value(self) -> str | None:
        """Return the value entered by the user (or the predefined answer)."""
        return self._answer

    def render(self, context: PromptContext | None = None) -> None:
        from wexample_prompt.common.prompt_context import PromptContext
        from wexample_prompt.common.prompt_response_line import PromptResponseLine
        from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
        from wexample_prompt.enums.terminal_color import TerminalColor
        from wexample_prompt.enums.text_style import TextStyle

        context = PromptContext.create_if_none(context=context)

        # Non-interactive mode: return the predefined answer immediately.
        if self.predefined_answer is not None:
            self._answer = str(self.predefined_answer)
            return

        # Build the question line (same style as ConfirmPromptResponse).
        question_lines = PromptResponseLine.create_from_string(self.question)
        _bold = [TextStyle.BOLD]  # hoisted: avoids a new list allocation per segment
        self.lines = []

        if question_lines:
            # Peel the first line so the "? " prefix check is not repeated inside
            # the loop on every subsequent iteration.
            first = question_lines[0]
            self.lines.append(PromptResponseLine(segments=[
                PromptResponseSegment(text="? ", color=TerminalColor.BLUE, styles=_bold),
            ] + [
                PromptResponseSegment(
                    text=seg.text,
                    color=seg.color or TerminalColor.LIGHT_WHITE,
                    styles=seg.styles or _bold,
                )
                for seg in first.segments
            ]))
            for q_line in question_lines[1:]:
                self.lines.append(PromptResponseLine(segments=[
                    PromptResponseSegment(
                        text=seg.text,
                        color=seg.color or TerminalColor.LIGHT_WHITE,
                        styles=seg.styles or _bold,
                    )
                    for seg in q_line.segments
                ]))

        # Print the question block.
        self._print_render(context=context)

        # Build the inline prompt string for input().
        if self.default_value is not None:
            prompt_str = f"  [{self.default_value}] "
        else:
            prompt_str = "  "

        raw = input(prompt_str).strip()
        if raw == "" and self.default_value is not None:
            self._answer = self.default_value
        else:
            self._answer = raw or None
