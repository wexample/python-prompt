from typing import ClassVar

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse
from wexample_prompt.enums.message_type import MessageType


class ErrorPromptResponse(BaseMessageResponse):
    """Response for error messages."""
    
    SYMBOL: ClassVar[str] = "❌"
    
    @classmethod
    def create(cls, text: str) -> 'ErrorPromptResponse':
        """Create an error message.
        
        Args:
            text (str): The error message text
            
        Returns:
            ErrorPromptResponse: A new error response
        """
        return cls._create_symbol_message(text, TerminalColor.RED)
    
    @classmethod
    def get_message_type(cls) -> MessageType:
        """Get the message type for error messages."""
        return MessageType.ERROR
