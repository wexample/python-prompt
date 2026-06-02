"""Multi-line free-text input response."""

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
class MultilineInputPromptResponse(AbstractInteractivePromptResponse):
    """Prompt the user for a multi-line free-text value.

    Key bindings:
      - Enter        → submit
      - Esc+Enter    → insert newline
      - Alt+Enter    → insert newline (alias)
      - Ctrl+C / Ctrl+D → return None
    """

    bordered: bool = public_field(
        default=False,
        description="Frame the input area with horizontal separators above and below.",
    )
    default_value: str | None = public_field(
        default=None,
        description="Pre-filled text shown in the editor; user can edit or accept it.",
    )
    footer_hint: str | None = public_field(
        default=None,
        description="Dim helper text shown below the bottom separator (only with bordered=True).",
    )
    predefined_answer: Any = public_field(
        default=None,
        description="Skip stdin and return this value directly (non-interactive / testing)",
    )
    prompt_prefix: str = public_field(
        default="❯ ",
        description="Inline prefix shown left of the cursor on the first line",
    )
    question: LineMessage | None = public_field(
        default="Type your message (Esc+Enter for newline, Enter to submit):",
        description="Prompt header shown above the cursor. Pass None to skip (useful with bordered=True).",
    )

    @classmethod
    def create_multiline_input(
        cls,
        question: LineMessage | None = "Type your message (Esc+Enter for newline, Enter to submit):",
        default_value: str | None = None,
        predefined_answer: Any = None,
        prompt_prefix: str = "❯ ",
        bordered: bool = False,
        footer_hint: str | None = None,
        reset_on_finish: bool = False,
    ) -> MultilineInputPromptResponse:
        return cls(
            question=question,
            default_value=default_value,
            predefined_answer=predefined_answer,
            prompt_prefix=prompt_prefix,
            bordered=bordered,
            footer_hint=footer_hint,
            reset_on_finish=reset_on_finish,
        )

    @classmethod
    def get_example_class(cls) -> type:
        from wexample_prompt.example.response.interactive.multiline_input_example import (
            MultilineInputExample,
        )

        return MultilineInputExample

    def get_value(self) -> str | None:
        return self._answer

    def render(self, context: PromptContext | None = None) -> None:
        from wexample_prompt.common.prompt_context import PromptContext
        from wexample_prompt.common.prompt_response_line import PromptResponseLine
        from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
        from wexample_prompt.enums.terminal_color import TerminalColor
        from wexample_prompt.enums.text_style import TextStyle

        context = PromptContext.create_if_none(context=context)

        if self.predefined_answer is not None:
            self._answer = str(self.predefined_answer)
            return

        if self.question:
            # Build the question line (consistent with InputPromptResponse styling).
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

            self._print_render(context=context)

        self._answer = self._read_multiline_input(context=context)

    def _read_multiline_input(self, context: PromptContext) -> str | None:
        from wexample_prompt.helper.input_widget import DEFAULT_INFO, InputWidget

        widget = InputWidget(
            initial=self.default_value or "",
            bordered=self.bordered,
            info=self.footer_hint if self.footer_hint is not None else DEFAULT_INFO,
            prompt_prefix=self.prompt_prefix,
        )
        text, validated = widget.run()
        if not validated:
            return None
        return text if text else None
