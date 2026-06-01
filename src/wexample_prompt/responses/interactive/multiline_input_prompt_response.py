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

    default_value: str | None = public_field(
        default=None,
        description="Pre-filled text shown in the editor; user can edit or accept it.",
    )
    predefined_answer: Any = public_field(
        default=None,
        description="Skip stdin and return this value directly (non-interactive / testing)",
    )
    prompt_prefix: str = public_field(
        default="❯ ",
        description="Inline prefix shown left of the cursor on the first line",
    )
    question: LineMessage = public_field(
        default="Type your message (Esc+Enter for newline, Enter to submit):",
        description="Prompt header shown above the cursor",
    )

    @classmethod
    def create_multiline_input(
        cls,
        question: LineMessage = "Type your message (Esc+Enter for newline, Enter to submit):",
        default_value: str | None = None,
        predefined_answer: Any = None,
        prompt_prefix: str = "❯ ",
        reset_on_finish: bool = False,
    ) -> MultilineInputPromptResponse:
        return cls(
            question=question,
            default_value=default_value,
            predefined_answer=predefined_answer,
            prompt_prefix=prompt_prefix,
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
        self._answer = self._read_multiline_input()

    def _read_multiline_input(self) -> str | None:
        from prompt_toolkit import PromptSession
        from prompt_toolkit.key_binding import KeyBindings

        bindings = KeyBindings()

        @bindings.add("escape", "enter")
        def _newline_on_esc_enter(event):  # noqa: ANN001
            event.current_buffer.insert_text("\n")

        @bindings.add("enter")
        def _submit_on_enter(event):  # noqa: ANN001
            event.current_buffer.validate_and_handle()

        session: PromptSession[Any] = PromptSession()
        try:
            text = session.prompt(
                message=self.prompt_prefix,
                default=self.default_value or "",
                multiline=True,
                key_bindings=bindings,
            )
        except (KeyboardInterrupt, EOFError):
            return None

        return text if text else None
