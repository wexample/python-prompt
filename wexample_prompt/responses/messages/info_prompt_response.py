from typing import ClassVar

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse
from wexample_prompt.enums.message_type import MessageType


class InfoPromptResponse(BaseMessageResponse):
    """Response for info messages."""
    
    SYMBOL: ClassVar[str] = "ℹ️"
    
    @classmethod
    def create(cls, text: str) -> 'InfoPromptResponse':
        """Create an info message.
        
        Args:
            text (str): The info message text
            
        Returns:
            InfoPromptResponse: A new info response
        """
        return cls._create_symbol_message(text, TerminalColor.LIGHT_BLUE)
    
    @classmethod
    def get_message_type(cls) -> MessageType:
        """Get the message type for info messages."""
        return MessageType.INFO
