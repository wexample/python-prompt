from typing import ClassVar

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse
from wexample_prompt.enums.message_type import MessageType


class CriticalPromptResponse(BaseMessageResponse):
    """Response for critical messages."""
    
    SYMBOL: ClassVar[str] = "💥"
    
    @classmethod
    def create(cls, text: str) -> 'CriticalPromptResponse':
        """Create a critical message.
        
        Args:
            text (str): The critical message text
            
        Returns:
            CriticalPromptResponse: A new critical response
        """
        return cls._create_symbol_message(text, TerminalColor.LIGHT_RED)
    
    @classmethod
    def get_message_type(cls) -> MessageType:
        """Get the message type for critical messages."""
        return MessageType.CRITICAL
