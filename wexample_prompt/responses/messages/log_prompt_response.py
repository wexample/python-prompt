from typing import Type, TYPE_CHECKING

from wexample_prompt.example.abstract_response_example import AbstractResponseExample
from wexample_prompt.responses.messages.abstract_message_response import AbstractMessageResponse

if TYPE_CHECKING:
    from wexample_prompt.enums.terminal_color import TerminalColor


class LogPromptResponse(AbstractMessageResponse):
    """Response for log messages."""

    @classmethod
    def create_log(
            cls: "LogPromptResponse",
            message: str,
            color: "TerminalColor" = None
    ) -> "LogPromptResponse":
        from wexample_prompt.enums.terminal_color import TerminalColor
        from wexample_prompt.common.prompt_response_line import PromptResponseLine

        return cls(
            lines=[
                PromptResponseLine.create_from_string(
                    text=message,
                    color=color or TerminalColor.WHITE
                )
            ],
        )

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        from wexample_prompt.example.response.messages.log_example import LogExample
        return LogExample
