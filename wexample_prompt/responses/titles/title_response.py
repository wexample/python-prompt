"""Title response implementation."""
from typing import Optional

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.titles.base_title_response import BaseTitleResponse


class TitleResponse(BaseTitleResponse):
    """Response for main titles with arrow prefix."""

    @classmethod
    def create_title(
        cls,
        text: str,
        color: Optional[TerminalColor] = TerminalColor.CYAN,
        fill_char: str = "⎯"
    ) -> 'TitleResponse':
        return super()._create(text=text, color=color, fill_char=fill_char)
    
    @classmethod
    def get_prefix(cls) -> str:
        return "▶"
