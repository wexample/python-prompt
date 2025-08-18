from typing import Type, Optional, TYPE_CHECKING, ClassVar

from pydantic import Field

from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.example.abstract_response_example import AbstractResponseExample
from wexample_prompt.responses.messages.abstract_message_response import AbstractMessageResponse

if TYPE_CHECKING:
    from wexample_prompt.enums.terminal_color import TerminalColor


class TitlePromptResponse(AbstractMessageResponse):
    PREFIX: ClassVar[str] = "❯"

    prefix_segment: PromptResponseSegment = Field(
        description="The prefix segment used by render process"
    )
    text_segment: PromptResponseSegment = Field(
        description="The title text segment"
    )

    @classmethod
    def create_title(
            cls: "TitlePromptResponse",
            text: str,
            color: Optional["TerminalColor"] = None,
    ) -> "TitlePromptResponse":
        from wexample_prompt.common.prompt_response_line import PromptResponseLine

        prefix_segment = PromptResponseSegment(
            text=f"{TitlePromptResponse.PREFIX} ",
            color=color
        )
        text_segment = PromptResponseSegment(
            text=text,
            color=color
        )

        return cls(
            prefix_segment=prefix_segment,
            text_segment=text_segment,
            lines=[
                PromptResponseLine(
                    segments=[
                        prefix_segment,
                        text_segment,
                    ]
                )
            ],
        )

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        from wexample_prompt.example.response.titles.title_example import TitleExample
        return TitleExample
