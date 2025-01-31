from typing import Optional, Any, TYPE_CHECKING

from wexample_prompt.mixins.with_io_manager import WithIoManager
from wexample_prompt.protocol.io_handler_protocol import IoHandlerProtocol

if TYPE_CHECKING:
    from wexample_prompt.responses.titles.title_prompt_response import TitlePromptResponse
    from wexample_prompt.responses.titles.subtitle_prompt_response import SubtitlePromptResponse
    from wexample_prompt.responses.list_prompt_response import ListPromptResponse
    from wexample_prompt.responses.table_prompt_response import TablePromptResponse


class WithPromptContext(WithIoManager, IoHandlerProtocol):
    prompt_context_parent: Optional[Any] = None
    _context_indent: int = 2  # Number of spaces for each indentation level

    def get_prompt_context_parent(self) -> Optional['WithPromptContext']:
        """Get the parent context for indentation. By default, returns None."""
        return self.prompt_context_parent

    def set_prompt_context_parent(self, parent: 'WithPromptContext') -> None:
        """Set the parent context for indentation."""
        self.prompt_context_parent = parent

    def get_context_indent_level(self) -> int:
        """Calculate the indentation level based on parent contexts."""
        parent = self.get_prompt_context_parent()
        if parent is None:
            return 0
        return parent.get_context_indent_level() + 1

    def format_message(self, message: str) -> str:
        """Format the message according to the bullet point style."""
        indent = " " * (self.get_context_indent_level() * self._context_indent)
        context_name = self.__class__.__name__

        if self.io._last_context != context_name:
            self.io._last_context = context_name
            return f"{indent}• {context_name}: {message}"

        return f"{indent}  ⋮ {message}"

    def log(self, message: str, **kwargs) -> None:
        """Format and send a message through the IO manager."""
        formatted_message = self.format_message(message)
        self.io.log(formatted_message, **kwargs)

    def debug(self, message: str, **kwargs) -> None:
        formatted_message = self.format_message(message)
        self.io.debug(formatted_message, **kwargs)

    def info(self, message: str, **kwargs) -> None:
        formatted_message = self.format_message(message)
        self.io.info(formatted_message, **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        formatted_message = self.format_message(message)
        self.io.warning(formatted_message, **kwargs)

    def error(self, message: str, **kwargs) -> None:
        formatted_message = self.format_message(message)
        self.io.error(formatted_message, **kwargs)

    def title(self, message: str, **kwargs) -> "TitlePromptResponse":
        formatted_message = self.format_message(message)
        return self.io.title(formatted_message, **kwargs)

    def subtitle(self, message: str, **kwargs) -> "SubtitlePromptResponse":
        formatted_message = self.format_message(message)
        return self.io.subtitle(formatted_message, **kwargs)

    def list(self, items: list, **kwargs) -> "ListPromptResponse":
        return self.io.list(items, **kwargs)

    def table(self, data: list, **kwargs) -> "TablePromptResponse":
        return self.io.table(data, **kwargs)
