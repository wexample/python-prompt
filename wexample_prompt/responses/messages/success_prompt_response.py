from typing import List, ClassVar

from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment


class SuccessPromptResponse(BaseMessageResponse):
    """Response for success messages with checkmark symbol."""
    
    CHECKMARK: ClassVar[str] = "✔"
    
    @classmethod
    def create(cls, text: str) -> 'SuccessPromptResponse':
        """Create a success message with a checkmark symbol.
        
        Args:
            text (str): The success message text
            
        Returns:
            SuccessPromptResponse: A new success response with checkmark
        """
        # Create the checkmark segment
        checkmark = PromptResponseSegment(text=f"{cls.CHECKMARK} ")
        
        # Create the message segment
        message = PromptResponseSegment(text=text)
        
        # Create a line with both segments
        line = PromptResponseLine(
            segments=[checkmark, message],
            line_type=cls.get_message_type()
        )
        
        return cls(lines=[line], message_type=cls.get_message_type())
    
    @classmethod
    def get_message_type(cls) -> MessageType:
        """Get the message type for success messages."""
        return MessageType.SUCCESS
