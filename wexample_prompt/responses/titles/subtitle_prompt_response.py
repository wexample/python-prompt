"""Subtitle response implementation."""
from typing import Optional, ClassVar

from typing_extensions import TYPE_CHECKING

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.titles.abstract_title_response import AbstractTitleResponse

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext


class SubtitlePromptResponseIoManagerMixin:
    """Mixin for IoManager to handle subtitle responses."""

    def subtitle(self, message: str, **kwargs) -> "SubtitlePromptResponse":
        """Create and display a subtitle response."""
        response = SubtitlePromptResponse.create_subtitle(
            text=message,
            context=self._create_context(),
        )

        if self._logger.handlers:
            self._logger.debug(message)

        self.print_response(response)
        return response


class SubtitlePromptResponsePromptContextMixin:
    """Mixin for WithPromptContext to handle subtitle responses with context formatting."""

    def subtitle(self, message: str, **kwargs) -> "SubtitlePromptResponse":
        """Create and display a subtitle response with context formatting."""
        formatted_message = self.format_message(message)
        return self.io.subtitle(formatted_message, **kwargs)


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
