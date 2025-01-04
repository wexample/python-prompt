"""Warning response implementation."""
import traceback
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
        text: str,
        context: Optional[ErrorContext] = None,
    ) -> 'WarningPromptResponse':
        """Create a warning message.
        
        Args:
            text: The warning message text
            context: Optional error context for handling behavior
            
        Returns:
            WarningPromptResponse: A new warning response
            
        Note:
            If context.trace is True, stack trace will be included in the message
        """
        # Create default context if none provided
        if context is None:
            context = ErrorContext(trace=False)  # Warnings don't trace by default
            
        # Format message with parameters if any
        message = context.format_message(text)
        
        # Add stack trace if requested
        if context.trace:
            message = f"{message}\n{traceback.format_exc()}"
            
        return cls._create_symbol_message(message, TerminalColor.YELLOW)
    
    @classmethod
    def get_message_type(cls) -> MessageType:
        """Get the message type for warning messages."""
        return MessageType.WARNING
