from typing import ClassVar

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse
from wexample_prompt.enums.message_type import MessageType


class DebugPromptResponse(BaseMessageResponse):
    """Response for debug messages."""
    
    SYMBOL: ClassVar[str] = "🔍"
    
    @classmethod
    def create(cls, text: str) -> 'DebugPromptResponse':
        """Create a debug message.
        
        Args:
            text (str): The debug message text
            
        Returns:
            DebugPromptResponse: A new debug response
        """
        return cls._create_symbol_message(text, TerminalColor.CYAN)
    
    @classmethod
    def get_message_type(cls) -> MessageType:
        """Get the message type for debug messages."""
        return MessageType.DEBUG
