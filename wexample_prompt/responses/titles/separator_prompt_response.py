from typing import TYPE_CHECKING, ClassVar, Optional, Type

from pydantic import Field

from wexample_prompt.common.prompt_response_segment import \
    PromptResponseSegment
from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.example.abstract_response_example import \
    AbstractResponseExample
from wexample_prompt.responses.messages.abstract_message_response import \
    AbstractMessageResponse

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.enums.terminal_color import TerminalColor


class SeparatorPromptResponse(AbstractMessageResponse):
    DEFAULT_CHARACTER: ClassVar[str] = "~"

    """Response for log messages."""
    character: Optional[str] = Field(
        default=DEFAULT_CHARACTER, description="The character to repeat"
    )
    label: Optional[str] = Field(
        default=None, description="A label to display on the separator right"
    )
    width: Optional[int] = Field(
        default=None, description="A fixed width, use context width if not provided"
    )
    separator_response_segment: PromptResponseSegment = Field(
        description="The line segment used by render process"
    )
    separator_response_label: Optional[PromptResponseSegment] = Field(
        default=None, description="The label displayed at the right"
    )

    @classmethod
    def create_separator(
        cls: "SeparatorPromptResponse",
        label: Optional[str] = None,
        width: Optional[int] = None,
        color: "TerminalColor" = None,
        character: Optional[str] = None,
        verbosity: VerbosityLevel = VerbosityLevel.DEFAULT,
    ) -> "SeparatorPromptResponse":
        from wexample_prompt.common.prompt_response_line import \
            PromptResponseLine
        from wexample_prompt.common.prompt_response_segment import \
            PromptResponseSegment

        segments = []

        separator_response_segment = PromptResponseSegment(text="-", color=color)
        segments.append(separator_response_segment)

        separator_response_label = None
        if label:
            separator_response_label = PromptResponseSegment(
                text=f" {label}", color=color
            )

            segments.append(separator_response_label)

        return cls(
            separator_response_segment=separator_response_segment,
            separator_response_label=separator_response_label,
            label=label,
            width=width,
            character=character or SeparatorPromptResponse.DEFAULT_CHARACTER,
            lines=[PromptResponseLine(segments=segments)],
            verbosity=verbosity,
        )

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        from wexample_prompt.example.response.titles.separator_example import \
            SeparatorExample

        return SeparatorExample

    def render(self, context: Optional["PromptContext"] = None) -> Optional[str]:
        width = self.width or context.get_width()
        length = width - len(context.render_indentation_text())
        if self.separator_response_label:
            length -= len(self.separator_response_label.text)

        self.separator_response_segment.text = length * self.character

        return super().render(
            context=context,
        )
