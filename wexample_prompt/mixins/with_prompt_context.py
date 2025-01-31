from typing import Optional, Any

from wexample_prompt.mixins.with_io_manager import WithIoManager
from wexample_prompt.protocol.io_handler_protocol import IoHandlerProtocol
from wexample_prompt.responses.titles.title_prompt_response import TitlePromptResponsePromptContextMixin
from wexample_prompt.responses.titles.subtitle_prompt_response import SubtitlePromptResponsePromptContextMixin
from wexample_prompt.responses.messages.log_prompt_response import LogPromptResponsePromptContextMixin


class WithPromptContext(
    WithIoManager,
    IoHandlerProtocol,
    TitlePromptResponsePromptContextMixin,
    SubtitlePromptResponsePromptContextMixin,
    LogPromptResponsePromptContextMixin
):
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

    def _format_if_message(self, message: Optional[str]) -> Optional[str]:
        """Format message if it exists, otherwise return None."""
        return self.format_message(message) if message else None

    # Override methods from AllResponsesMixin to add context formatting
    def log(self, message: str, **kwargs) -> "LogPromptResponse":
        formatted_message = self.format_message(message)
        return self.io.log(formatted_message, **kwargs)

    def info(self, message: str, **kwargs) -> "InfoPromptResponse":
        formatted_message = self.format_message(message)
        return self.io.info(formatted_message, **kwargs)

    def debug(self, message: str, **kwargs) -> "DebugPromptResponse":
        formatted_message = self.format_message(message)
        return self.io.debug(formatted_message, **kwargs)

    def error(self, message: str, **kwargs) -> "ErrorPromptResponse":
        formatted_message = self.format_message(message)
        return self.io.error(formatted_message, **kwargs)

    def warning(self, message: str, **kwargs) -> "WarningPromptResponse":
        formatted_message = self.format_message(message)
        return self.io.warning(formatted_message, **kwargs)

    def title(self, message: str, **kwargs) -> "TitlePromptResponse":
        formatted_message = self.format_message(message)
        return self.io.title(formatted_message, **kwargs)

    def subtitle(self, message: str, **kwargs) -> "SubtitlePromptResponse":
        formatted_message = self.format_message(message)
        return self.io.subtitle(formatted_message, **kwargs)

    def success(self, message: str, **kwargs) -> "SuccessPromptResponse":
        formatted_message = self.format_message(message)
        return self.io.success(formatted_message, **kwargs)

    def failure(self, message: str, **kwargs) -> "FailurePromptResponse":
        formatted_message = self.format_message(message)
        return self.io.failure(formatted_message, **kwargs)

    def task(self, message: str, **kwargs) -> "TaskPromptResponse":
        formatted_message = self.format_message(message)
        return self.io.task(formatted_message, **kwargs)

    # Methods that don't need message formatting
    def list(self, items: list, **kwargs) -> "ListPromptResponse":
        return self.io.list(items, **kwargs)

    def table(self, data: list, **kwargs) -> "TablePromptResponse":
        return self.io.table(data, **kwargs)

    def tree(self, data: Dict[str, Any], **kwargs) -> "TreePromptResponse":
        return self.io.tree(data, **kwargs)

    def properties(self, properties: Dict[str, Any], **kwargs) -> "PropertiesPromptResponse":
        return self.io.properties(properties, **kwargs)

    def suggestions(self, suggestions: List[str], **kwargs) -> "SuggestionsPromptResponse":
        return self.io.suggestions(suggestions, **kwargs)

    # Methods that have optional messages
    def progress(self, total: int, message: Optional[str] = None, **kwargs) -> "ProgressPromptResponse":
        formatted_message = self._format_if_message(message)
        return self.io.progress(total, message=formatted_message, **kwargs)

    def choice(self, choices: List[str], message: Optional[str] = None, **kwargs) -> "ChoicePromptResponse":
        formatted_message = self._format_if_message(message)
        return self.io.choice(choices, message=formatted_message, **kwargs)

    def choice_dict(self, choices: Dict[str, Any], message: Optional[str] = None, **kwargs) -> "ChoiceDictPromptResponse":
        formatted_message = self._format_if_message(message)
        return self.io.choice_dict(choices, message=formatted_message, **kwargs)

    def multiple(self, responses: List[Any], **kwargs) -> "MultiplePromptResponse":
        return self.io.multiple(responses, **kwargs)

    def file_picker(self, path: str, pattern: Optional[str] = None, **kwargs) -> "FilePickerPromptResponse":
        return self.io.file_picker(path, pattern=pattern, **kwargs)

    def dir_picker(self, path: str, **kwargs) -> "DirPickerPromptResponse":
        return self.io.dir_picker(path, **kwargs)
