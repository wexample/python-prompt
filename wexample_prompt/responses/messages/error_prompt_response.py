from typing import ClassVar, Optional

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.common.error_context import ErrorContext


class ErrorPromptResponse(BaseMessageResponse):
    SYMBOL: ClassVar[str] = "❌"

    @classmethod
    def create(
        cls,
        message: str,
        context: Optional[ErrorContext] = None,
    ) -> 'ErrorPromptResponse':
        # Create response with context
        return cls._create_symbol_message(
            text=message,
            color=TerminalColor.RED,
            context=context
        )

    @classmethod
    def get_message_type(cls) -> MessageType:
        """Get the message type for error messages."""
        return MessageType.ERROR
