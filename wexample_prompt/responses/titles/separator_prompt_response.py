from typing import Type

from wexample_prompt.example.abstract_response_example import AbstractResponseExample
from wexample_prompt.responses.messages.abstract_message_response import AbstractMessageResponse


class SeparatorPromptResponse(AbstractMessageResponse):
    """Response for log messages."""

    @classmethod
    def create_separator(
            cls: "SeparatorPromptResponse",
    ) -> "SeparatorPromptResponse":
        from wexample_prompt.enums.terminal_color import TerminalColor
        from wexample_prompt.common.prompt_response_line import PromptResponseLine

        return cls(
            lines=[
                PromptResponseLine.create_from_string(
                    text="----",
                    color=TerminalColor.WHITE
                )
            ],
        )

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        from wexample_prompt.example.response.titles.separator_example import SeparatorExample
        return SeparatorExample
