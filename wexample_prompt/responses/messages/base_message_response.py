from typing import Optional, List
from wexample_prompt.responses.base_prompt_response import BasePromptResponse
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment


class BaseMessageResponse(BasePromptResponse):
    """Base class for message type responses."""
    
    @classmethod
    def create(cls, text: str) -> 'BaseMessageResponse':
        """Create a message response with the appropriate message type."""
        segment = PromptResponseSegment(text=text)
        line = PromptResponseLine(segments=[segment], line_type=cls.get_message_type())
        return cls(lines=[line], message_type=cls.get_message_type())
    
    @classmethod
    def get_message_type(cls) -> MessageType:
        """Get the message type for this response class. Should be overridden by subclasses."""
        raise NotImplementedError("Subclasses must implement get_message_type()")
