from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_prompt.responses.titles.subtitle_prompt_response import SubtitlePromptResponse


class SubtitlePromptResponsePromptContextMixin:
    """Mixin for WithPromptContext to handle subtitle responses with context formatting."""

    def subtitle(self, message: str, **kwargs) -> "SubtitlePromptResponse":
        """Create and display a subtitle response with context formatting."""
        formatted_message = self.format_message(message)
        return self.io.subtitle(formatted_message, **kwargs)
