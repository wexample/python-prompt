from typing import ClassVar, Optional, Any

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.common.error_context import ErrorContext


class ErrorPromptResponse(BaseMessageResponse):
    SYMBOL: ClassVar[str] = "❌"
    exception: Optional[Any] = None

    @classmethod
    def create(
        cls,
        message: str,
        context: Optional[ErrorContext] = None,
        exception=None
    ) -> 'ErrorPromptResponse':
        # Create response with context
        response = cls._create_symbol_message(
            text=message,
            color=TerminalColor.RED,
            context=context
        )

        response.exception = exception

        return response

    def _on_fatal(self):
        raise self.exception

    @classmethod
    def get_message_type(cls) -> MessageType:
        """Get the message type for error messages."""
        return MessageType.ERROR
