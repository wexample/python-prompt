from typing import ClassVar

from wexample_prompt.common.color_manager import ColorManager
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment


class WarningPromptResponse(BaseMessageResponse):
    """Response for warning messages."""
    
    WARNING_SYMBOL: ClassVar[str] = "⚠"
    
    @classmethod
    def create(cls, text: str) -> 'WarningPromptResponse':
        """Create a warning message.
        
        Args:
            text (str): The warning message text
            
        Returns:
            WarningPromptResponse: A new warning response
        """
        # Create the warning symbol with color
        symbol = PromptResponseSegment(
            text=ColorManager.colorize(f"{cls.WARNING_SYMBOL} ", TerminalColor.YELLOW, TerminalColor.BOLD)
        )
        
        # Create the message segment with color
        message = PromptResponseSegment(
            text=ColorManager.colorize(text, TerminalColor.YELLOW)
        )
        
        # Create a line with both segments
        line = PromptResponseLine(
            segments=[symbol, message],
            line_type=cls.get_message_type()
        )
        
        return cls(lines=[line], message_type=cls.get_message_type())
    
    @classmethod
    def get_message_type(cls) -> MessageType:
        """Get the message type for warning messages."""
        return MessageType.WARNING
