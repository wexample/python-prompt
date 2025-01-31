"""Title response implementation."""
from typing import Optional, TYPE_CHECKING, ClassVar

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.titles.abstract_title_response import AbstractTitleResponse

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext


class TitlePromptResponseIoManagerMixin:
    """Mixin for IoManager to handle title responses."""

    def title(self, message: str, **kwargs) -> "TitlePromptResponse":
        """Create and display a title response."""
        response = TitlePromptResponse.create_title(
            text=message,
            context=self._create_context(),
        )

        if self._logger.handlers:
            self._logger.debug(message)

        self.print_response(response)
        return response


class TitlePromptResponsePromptContextMixin:
    """Mixin for WithPromptContext to handle title responses with context formatting."""

    def title(self, message: str, **kwargs) -> "TitlePromptResponse":
        """Create and display a title response with context formatting."""
        formatted_message = self.format_message(message)
        return self.io.title(formatted_message, **kwargs)


class TitlePromptResponse(
    AbstractTitleResponse,
    TitlePromptResponseIoManagerMixin,
    TitlePromptResponsePromptContextMixin
):
    """Response for main titles with arrow prefix."""

    TITLE_CHAR: ClassVar[str] = "="

    @classmethod
    def create_title(
        cls,
        text: str,
        context: Optional[PromptContext] = None,
        color: Optional[TerminalColor] = TerminalColor.CYAN,
        fill_char: Optional[str] = None
    ) -> 'TitlePromptResponse':
        return super()._create_title(
            text=text,
            color=color,
            fill_char=fill_char,
            context=context
        )

    @classmethod
    def get_prefix(cls) -> str:
        return "❯"
