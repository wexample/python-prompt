from typing import Optional

from colorama import init, Style

from wexample_prompt.enums.terminal_color import TerminalColor


class ColorManager:
    """Manages color application and terminal capabilities."""
    
    # Initialize colorama when class is loaded
    init()

    @classmethod
    def colorize(cls, text: str, color: Optional[TerminalColor] = None,
                 style: Optional[TerminalColor] = None) -> str:
        prefix = ''
        if color:
            prefix += str(color)
        if style:
            prefix += str(style)

        if prefix:
            return f"{prefix}{text}{Style.RESET_ALL}"
        return text
