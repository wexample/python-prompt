from typing import ClassVar

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse
from wexample_prompt.enums.message_type import MessageType


class FailurePromptResponse(BaseMessageResponse):
    """Response for failure messages."""
    
    SYMBOL: ClassVar[str] = "❌"
    
    @classmethod
    def create(cls, text: str) -> 'FailurePromptResponse':
        """Create a failure message.
        
        Args:
            text (str): The failure message text
            
        Returns:
            FailurePromptResponse: A new failure response
        """
        return cls._create_symbol_message(text, TerminalColor.RED)
    
    @classmethod
    def get_message_type(cls) -> MessageType:
        """Get the message type for failure messages."""
        return MessageType.FAILURE
