from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_prompt.responses.titles.title_prompt_response import TitlePromptResponse


class TitlePromptResponsePromptContextMixin:
    """Mixin for WithPromptContext to handle title responses with context formatting."""

    def title(self, message: str, **kwargs) -> "TitlePromptResponse":
        """Create and display a title response with context formatting."""
        formatted_message = self.format_message(message)
        return self.io.title(formatted_message, **kwargs)
