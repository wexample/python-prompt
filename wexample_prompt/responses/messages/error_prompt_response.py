"""Error response implementation."""
import sys
import traceback
from typing import ClassVar, Optional, Dict, Any, Union

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.common.error_context import ErrorContext


class ErrorPromptResponse(BaseMessageResponse):
    """Response for error messages."""
    
    SYMBOL: ClassVar[str] = "❌"
    
    @classmethod
    def create(
        cls,
        text: str,
        context: Optional[ErrorContext] = None,
    ) -> 'ErrorPromptResponse':
        """Create an error message.
        
        Args:
            text: The error message text
            context: Optional error context for handling behavior
            
        Returns:
            ErrorPromptResponse: A new error response
            
        Note:
            If context.fatal is True, this will exit the program with context.exit_code
            If context.trace is True, stack trace will be included in the message
        """
        # Create default context if none provided
        if context is None:
            context = ErrorContext()
            
        # Format message with parameters if any
        message = context.format_message(text) if text else "Unknown error"
            
        # Add stack trace if requested
        if context.trace:
            trace = traceback.format_exc()
            if trace and trace != 'NoneType: None\n':
                message = f"{message}\n{trace}"
            
        # Create response
        response = cls._create_symbol_message(message, TerminalColor.RED)
        
        # Exit if fatal
        if context.fatal:
            sys.exit(context.exit_code)
            
        return response
    
    @classmethod
    def get_message_type(cls) -> MessageType:
        """Get the message type for error messages."""
        return MessageType.ERROR
