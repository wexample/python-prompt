"""Title prompt response for displaying section titles."""
from typing import Optional

from wexample_prompt.common.color_manager import ColorManager
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.enums.response_type import ResponseType
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.enums.text_style import TextStyle
from wexample_prompt.responses.base_prompt_response import BasePromptResponse


class TitlePromptResponse(BasePromptResponse):
    """Response for displaying section titles."""
    
    @classmethod
    def create(
        cls,
        text: str,
        level: int = 1,
        symbol: Optional[str] = "===",
        color: Optional[TerminalColor] = TerminalColor.CYAN
    ) -> 'TitlePromptResponse':
        """Create a title message.
        
        Args:
            text (str): The title text
            level (int): Title level (1 for main titles, 2+ for subtitles)
            symbol (Optional[str]): Override the default symbol
            color (Optional[TerminalColor]): Color for the title
            
        Returns:
            TitlePromptResponse: A new title response
        """
        # Create the title with symbol and padding
        if level == 1:
            # Main title: === Title ===
            full_text = f"{symbol} {text} {symbol}"
            styles = [TextStyle.BOLD]
        else:
            # Subtitle: --- Title
            subtitle_symbol = "-" * len(symbol)
            full_text = f"{subtitle_symbol} {text}"
            styles = []
            
        # Create colored segment
        title_segment = PromptResponseSegment(
            text=ColorManager.colorize(full_text, color) if color else full_text,
            styles=styles
        )
        
        # Add empty lines for spacing
        empty_line = PromptResponseLine(segments=[PromptResponseSegment(text="")])
        title_line = PromptResponseLine(segments=[title_segment])
        
        # Return with padding
        return cls(
            lines=[empty_line, title_line, empty_line],
            response_type=ResponseType.TITLE,
            message_type=MessageType.LOG  # Use LOG as default message type
        )
