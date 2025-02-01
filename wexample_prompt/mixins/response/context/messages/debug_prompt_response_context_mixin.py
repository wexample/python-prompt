from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_prompt.responses.messages import DebugPromptResponse


class DebugPromptResponsePromptContextMixin:
    """Mixin for WithPromptContext to handle debug responses with context formatting."""

    def debug(self, message: str, **kwargs) -> "DebugPromptResponse":
        """Create and display a debug response with context formatting."""
        formatted_message = self.format_message(message)
        return self.io.debug(formatted_message, **kwargs)
