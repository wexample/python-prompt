from typing import Type, Optional, TYPE_CHECKING

from pydantic import Field

from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.example.abstract_response_example import AbstractResponseExample
from wexample_prompt.responses.messages.abstract_message_response import AbstractMessageResponse

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.enums.terminal_color import TerminalColor


class SeparatorPromptResponse(AbstractMessageResponse):
    """Response for log messages."""
    character: Optional[str] = Field(
        default="-",
        description="The character to repeat"
    )
    label: Optional[str] = Field(
        default=None,
        description="A label to display on the separator right"
    )
    width: Optional[int] = Field(
        default=None,
        description="A fixed width, use context width if not provided"
    )
    separator_response_segment: PromptResponseSegment = Field(
        default=None,
        description="The line segment used by render process"
    )

    @classmethod
    def create_separator(
            cls: "SeparatorPromptResponse",
            label: Optional[str] = None,
            width: Optional[int] = None,
            color: "TerminalColor" = None
    ) -> "SeparatorPromptResponse":
        from wexample_prompt.common.prompt_response_line import PromptResponseLine
        from wexample_prompt.common.prompt_response_segment import PromptResponseSegment

        separator_response_segment = PromptResponseSegment(
            text="-",
            color=color
        )

        return cls(
            separator_response_segment=separator_response_segment,
            label=label,
            width=width,
            lines=[
                PromptResponseLine(
                    segments=[
                        separator_response_segment
                    ]
                )
            ],
        )

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        from wexample_prompt.example.response.titles.separator_example import SeparatorExample
        return SeparatorExample

    def render(self, context: Optional["PromptContext"] = None) -> str:
        self.separator_response_segment.text = (context.width - len(context.render_indentation_text())) * self.character

        return super().render(
            context=context,
        )
