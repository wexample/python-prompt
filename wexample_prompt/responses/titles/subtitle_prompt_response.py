"""Subtitle response implementation."""
from typing import Optional, ClassVar

from typing_extensions import TYPE_CHECKING

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.titles.abstract_title_response import AbstractTitleResponse

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext


class SubtitlePromptResponse(AbstractTitleResponse):
    """Response for subtitles with small arrow prefix."""

    TITLE_CHAR: ClassVar[str] = "-"

    @classmethod
    def create_subtitle(
        cls,
        text: str,
        context: Optional["PromptContext"] = None,
        color: Optional[TerminalColor] = TerminalColor.BLUE,
        fill_char: Optional[str] = None,
    ) -> 'SubtitlePromptResponse':
        return super()._create_title(
            text=text,
            color=color,
            fill_char=fill_char,
            context=context or PromptContext()
        )

    @classmethod
    def get_prefix(cls) -> str:
        """Get the prefix character for the subtitle."""
        return "  ❯"
