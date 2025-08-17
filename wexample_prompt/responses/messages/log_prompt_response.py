"""Response for log messages."""
from typing import TYPE_CHECKING, Type

from wexample_prompt.example.abstract_response_example import AbstractResponseExample
from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse

if TYPE_CHECKING:
    pass


class LogPromptResponse(BaseMessageResponse):
    """Response for log messages."""

    @classmethod
    def create_log(
        cls: "LogPromptResponse",
        message: str,
    ) -> "LogPromptResponse":

        return cls(
        )

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        """Get the example class for log messages."""
        from wexample_prompt.example.response.messages.log_example import LogExample
        return LogExample