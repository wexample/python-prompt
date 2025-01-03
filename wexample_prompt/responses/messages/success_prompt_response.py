from typing import ClassVar

from wexample_prompt.common.color_manager import ColorManager
from wexample_prompt.enums.terminal_color import TerminalColor
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
        # Get the success color
        color = ColorManager.get_message_color(cls.get_message_type())
        
        # Create the checkmark segment with color
        checkmark = PromptResponseSegment(
            text=ColorManager.colorize(f"{cls.CHECKMARK} ", color, TerminalColor.BOLD)
        )
        
        # Create the message segment with color
        message = PromptResponseSegment(
            text=ColorManager.colorize(text, color)
        )
        
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
