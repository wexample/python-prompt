from typing import Optional

from wexample_prompt.mixins.with_io_manager import WithIoManager


class WithPromptContext(WithIoManager):
    prompt_context_parent: Optional['WithPromptContext'] = None
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

    def get_context_prefix(self) -> str:
        """Get the prefix for messages, including the class name."""
        return f"[{self.__class__.__name__}]"

    def get_context_indent(self) -> str:
        """Get the indentation string based on the context level."""
        return " " * (self.get_context_indent_level() * self._context_indent)

    def log(self, message: str, **kwargs) -> None:
        """Format and send a message through the IO manager with proper indentation and prefix."""
        formatted_message = f"{self.get_context_indent()}{self.get_context_prefix()} {message}"
        self.io.log(formatted_message, **kwargs)

    def debug(self, message: str, **kwargs) -> None:
        """Format and send a debug message with proper indentation and prefix."""
        formatted_message = f"{self.get_context_indent()}{self.get_context_prefix()} {message}"
        self.io.debug(formatted_message, **kwargs)

    def info(self, message: str, **kwargs) -> None:
        """Format and send an info message with proper indentation and prefix."""
        formatted_message = f"{self.get_context_indent()}{self.get_context_prefix()} {message}"
        self.io.info(formatted_message, **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        """Format and send a warning message with proper indentation and prefix."""
        formatted_message = f"{self.get_context_indent()}{self.get_context_prefix()} {message}"
        self.io.warning(formatted_message, **kwargs)

    def error(self, message: str, **kwargs) -> None:
        """Format and send an error message with proper indentation and prefix."""
        formatted_message = f"{self.get_context_indent()}{self.get_context_prefix()} {message}"
        self.io.error(formatted_message, **kwargs)
