from colorama import Style, init
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.enums.text_style import TextStyle


class ColorManager:
    """Manages color application and terminal capabilities."""

    # Initialize colorama when class is loaded
    init()

    @classmethod
    def colorize(
        cls,
        text: str,
        color: TerminalColor | None = None,
        style: TerminalColor | None = None,
    ) -> str:
        prefix = ""
        if color:
            prefix += str(color)
        if style:
            prefix += str(style)

        if prefix:
            return f"{prefix}{text}{Style.RESET_ALL}"
        return text

    @classmethod
    def get_style_ansi(cls, style: TextStyle) -> str:
        """Map TextStyle to ANSI code without reset."""
        style_codes = {
            TextStyle.BOLD: "\033[1m",
            TextStyle.ITALIC: "\033[3m",
            TextStyle.UNDERLINE: "\033[4m",
            TextStyle.STRIKETHROUGH: "\033[9m",
            TextStyle.DIM: "\033[2m",
            TextStyle.REVERSE: "\033[7m",
            TextStyle.HIDDEN: "\033[8m",
        }
        return style_codes.get(style, "")

    @classmethod
    def build_prefix(
        cls,
        color: TerminalColor | None = None,
        styles: list[TextStyle] | None = None,
    ) -> str:
        """Build ANSI prefix combining color and a list of TextStyle entries."""
        prefix = ""
        if color:
            prefix += str(color)
        if styles:
            prefix += "".join(cls.get_style_ansi(s) for s in styles)
        return prefix
