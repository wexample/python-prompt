import sys
import traceback
from typing import ClassVar, Optional

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.common.error_context import ErrorContext


class ErrorPromptResponse(BaseMessageResponse[ErrorContext]):
    SYMBOL: ClassVar[str] = "❌"
    
    @classmethod
    def create(
        cls,
        context: ErrorContext,
        text: str,
    ) -> 'ErrorPromptResponse':
        # Format message with parameters if any
        message = context.format_message(text) if text else "Unknown error"
            
        # Add stack trace if requested
        if context.trace:
            trace = traceback.format_exc()
            if trace and trace != 'NoneType: None\n':
                message = f"{message}\n{trace}"

        # Create response with context
        response = cls._create_symbol_message(message, TerminalColor.RED)
        response.context = context
        
        return response
    
    @classmethod
    def get_message_type(cls) -> MessageType:
        """Get the message type for error messages."""
        return MessageType.ERROR
