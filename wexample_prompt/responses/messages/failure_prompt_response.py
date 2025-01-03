from typing import List, ClassVar

from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment


class FailurePromptResponse(BaseMessageResponse):
    """Response for failure messages with X symbol."""
    
    X_MARK: ClassVar[str] = "×"
    
    @classmethod
    def create(cls, text: str) -> 'FailurePromptResponse':
        """Create a failure message with an X symbol.
        
        Args:
            text (str): The failure message text
            
        Returns:
            FailurePromptResponse: A new failure response with X mark
        """
        # Create the X mark segment
        x_mark = PromptResponseSegment(text=f"{cls.X_MARK} ")
        
        # Create the message segment
        message = PromptResponseSegment(text=text)
        
        # Create a line with both segments
        line = PromptResponseLine(
            segments=[x_mark, message],
            line_type=cls.get_message_type()
        )
        
        return cls(lines=[line], message_type=cls.get_message_type())
    
    @classmethod
    def get_message_type(cls) -> MessageType:
        """Get the message type for failure messages."""
        return MessageType.FAILURE
