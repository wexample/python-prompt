from typing import ClassVar, Optional

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.common.error_context import ErrorContext


class WarningPromptResponse(BaseMessageResponse):
    """Response for warning messages."""

    SYMBOL: ClassVar[str] = "⚠️"

    @classmethod
    def create(
        cls,
        message: str,
        context: Optional[ErrorContext] = None,
    ) -> 'WarningPromptResponse':
        return cls._create_symbol_message(
            text=message,
            color=TerminalColor.YELLOW,
            context=context or ErrorContext(trace=False)
        )

    @classmethod
    def get_message_type(cls) -> MessageType:
        """Get the message type for warning messages."""
        return MessageType.WARNING
