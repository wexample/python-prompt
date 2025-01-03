from typing import ClassVar

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse
from wexample_prompt.enums.message_type import MessageType


class SuccessPromptResponse(BaseMessageResponse):
    """Response for success messages."""
    
    SYMBOL: ClassVar[str] = "✅"
    
    @classmethod
    def create(cls, text: str) -> 'SuccessPromptResponse':
        """Create a success message.
        
        Args:
            text (str): The success message text
            
        Returns:
            SuccessPromptResponse: A new success response
        """
        return cls._create_symbol_message(text, TerminalColor.GREEN)
    
    @classmethod
    def get_message_type(cls) -> MessageType:
        """Get the message type for success messages."""
        return MessageType.SUCCESS
