"""Subtitle response implementation."""
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.titles.base_title_response import BaseTitleResponse


class SubtitleResponse(BaseTitleResponse):
    """Response for subtitles with small arrow prefix."""
    
    @classmethod
    def create(cls, text: str, color: TerminalColor = TerminalColor.BLUE) -> 'SubtitleResponse':
        """Create a subtitle response.
        
        Args:
            text (str): The subtitle text
            color (TerminalColor): Color for the subtitle, defaults to blue
            
        Returns:
            SubtitleResponse: A new subtitle response
        """
        return super().create(text=text, color=color, fill_char="-")
    
    @classmethod
    def get_prefix(cls) -> str:
        """Get the prefix for subtitles.
        
        Returns:
            str: The subtitle prefix (  ▷)
        """
        return "  ▷"
