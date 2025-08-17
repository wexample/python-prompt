"""Response for log messages."""
from typing import TYPE_CHECKING

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

