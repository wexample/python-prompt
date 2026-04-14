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
        self.lines = []

        for idx, q_line in enumerate(question_lines):
            segs = []
            if idx == 0:
                segs.append(
                    PromptResponseSegment(
                        text="? ",
                        color=TerminalColor.BLUE,
                        styles=[TextStyle.BOLD],
                    )
                )
            for seg in q_line.segments:
                segs.append(
                    PromptResponseSegment(
                        text=seg.text,
                        color=seg.color or TerminalColor.LIGHT_WHITE,
                        styles=seg.styles or [TextStyle.BOLD],
                    )
                )
            self.lines.append(PromptResponseLine(segments=segs))

        # Print the question block.
        self._print_render(context=context)

        # Build the inline prompt string for input().
        prompt_str = ""
        if self.default_value is not None:
            prompt_str = f"  [{self.default_value}] "
        else:
            prompt_str = "  "

        raw = input(prompt_str).strip()
        if raw == "" and self.default_value is not None:
            self._answer = self.default_value
        else:
            self._answer = raw or None
