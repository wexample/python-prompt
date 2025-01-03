from typing import ClassVar

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse
from wexample_prompt.enums.message_type import MessageType


class AlertPromptResponse(BaseMessageResponse):
    """Response for alert messages."""
    
    SYMBOL: ClassVar[str] = "🚨"
    
    @classmethod
    def create(cls, text: str) -> 'AlertPromptResponse':
        """Create an alert message.
        
        Args:
            text (str): The alert message text
            
        Returns:
            AlertPromptResponse: A new alert response
        """
        return cls._create_symbol_message(text, TerminalColor.YELLOW)
    
    @classmethod
    def get_message_type(cls) -> MessageType:
        """Get the message type for alert messages."""
        return MessageType.ALERT
