"""Subtitle response implementation."""
from typing import Optional

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.titles.base_title_response import BaseTitleResponse


class SubtitleResponse(BaseTitleResponse):
    """Response for subtitles with small arrow prefix."""
    
    @classmethod
    def create_subtitle(
        cls,
        text: str,
        color: Optional[TerminalColor] = TerminalColor.BLUE,
        fill_char: str = "-"
    ) -> 'SubtitleResponse':
        """Create a subtitle response.
        
        Args:
            text: The subtitle text
            color: Color for the subtitle, defaults to blue
            fill_char: Character to use for filling the line
            
        Returns:
            SubtitleResponse: A new subtitle response
        """
        return super()._create(text=text, color=color, fill_char=fill_char)
    
    @classmethod
    def get_prefix(cls) -> str:
        """Get the prefix for subtitles.
        
        Returns:
            str: The subtitle prefix (  ▷)
        """
        return "  ▷"
