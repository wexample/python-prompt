from typing import List, ClassVar

from wexample_prompt.common.color_manager import ColorManager
from wexample_prompt.enums.terminal_color import TerminalColor
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
        # Get the failure color
        color = ColorManager.get_message_color(cls.get_message_type())
        
        # Create the X mark segment with color
        x_mark = PromptResponseSegment(
            text=ColorManager.colorize(f"{cls.X_MARK} ", color, TerminalColor.BOLD)
        )
        
        # Create the message segment with color
        message = PromptResponseSegment(
            text=ColorManager.colorize(text, color)
        )
        
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
