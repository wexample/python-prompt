from typing import Optional, Any, TYPE_CHECKING, Dict, List, Union

from wexample_prompt.mixins.with_io_manager import WithIoManager
from wexample_prompt.protocol.io_handler_protocol import IoHandlerProtocol

if TYPE_CHECKING:
    from wexample_prompt.responses.titles.title_prompt_response import TitlePromptResponse
    from wexample_prompt.responses.titles.subtitle_prompt_response import SubtitlePromptResponse
    from wexample_prompt.responses.messages.log_prompt_response import LogPromptResponse
    from wexample_prompt.responses.messages.info_prompt_response import InfoPromptResponse
    from wexample_prompt.responses.messages.debug_prompt_response import DebugPromptResponse
    from wexample_prompt.responses.messages.error_prompt_response import ErrorPromptResponse
    from wexample_prompt.responses.messages.failure_prompt_response import FailurePromptResponse
    from wexample_prompt.responses.messages.success_prompt_response import SuccessPromptResponse
    from wexample_prompt.responses.messages.task_prompt_response import TaskPromptResponse
    from wexample_prompt.responses.messages.warning_prompt_response import WarningPromptResponse
    from wexample_prompt.responses.list_prompt_response import ListPromptResponse
    from wexample_prompt.responses.table_prompt_response import TablePromptResponse
    from wexample_prompt.responses.tree_prompt_response import TreePromptResponse
    from wexample_prompt.responses.properties_prompt_response import PropertiesPromptResponse
    from wexample_prompt.responses.suggestions_prompt_response import SuggestionsPromptResponse
    from wexample_prompt.responses.progress_prompt_response import ProgressPromptResponse
    from wexample_prompt.responses.multiple_prompt_response import MultiplePromptResponse
    from wexample_prompt.responses.interactive.choice_prompt_response import ChoicePromptResponse
    from wexample_prompt.responses.interactive.choice_dict_prompt_response import ChoiceDictPromptResponse
    from wexample_prompt.responses.interactive.file_picker_prompt_response import FilePickerPromptResponse
    from wexample_prompt.responses.interactive.dir_picker_prompt_response import DirPickerPromptResponse


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

    def log(self, message: str, **kwargs) -> "LogPromptResponse":
        """Format and send a message through the IO manager."""
        formatted_message = self.format_message(message)
        return self.io.log(formatted_message, **kwargs)

    def debug(self, message: str, **kwargs) -> "DebugPromptResponse":
        formatted_message = self.format_message(message)
        return self.io.debug(formatted_message, **kwargs)

    def info(self, message: str, **kwargs) -> "InfoPromptResponse":
        formatted_message = self.format_message(message)
        return self.io.info(formatted_message, **kwargs)

    def warning(self, message: str, **kwargs) -> "WarningPromptResponse":
        formatted_message = self.format_message(message)
        return self.io.warning(formatted_message, **kwargs)

    def error(self, message: str, exception: Optional[Exception] = None, fatal: bool = True, **kwargs) -> "ErrorPromptResponse":
        formatted_message = self.format_message(message)
        return self.io.error(formatted_message, exception=exception, fatal=fatal, **kwargs)

    def failure(self, message: str, **kwargs) -> "FailurePromptResponse":
        formatted_message = self.format_message(message)
        return self.io.failure(formatted_message, **kwargs)

    def success(self, message: str, **kwargs) -> "SuccessPromptResponse":
        formatted_message = self.format_message(message)
        return self.io.success(formatted_message, **kwargs)

    def task(self, message: str, **kwargs) -> "TaskPromptResponse":
        formatted_message = self.format_message(message)
        return self.io.task(formatted_message, **kwargs)

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

    def tree(self, data: Dict[str, Any], **kwargs) -> "TreePromptResponse":
        return self.io.tree(data, **kwargs)

    def properties(self, properties: Dict[str, Any], **kwargs) -> "PropertiesPromptResponse":
        return self.io.properties(properties, **kwargs)

    def suggestions(self, suggestions: List[str], **kwargs) -> "SuggestionsPromptResponse":
        return self.io.suggestions(suggestions, **kwargs)

    def progress(self, total: int, message: Optional[str] = None, **kwargs) -> "ProgressPromptResponse":
        if message:
            message = self.format_message(message)
        return self.io.progress(total, message=message, **kwargs)

    def multiple(self, responses: List[Any], **kwargs) -> "MultiplePromptResponse":
        return self.io.multiple(responses, **kwargs)

    def choice(self, choices: List[str], message: Optional[str] = None, **kwargs) -> "ChoicePromptResponse":
        if message:
            message = self.format_message(message)
        return self.io.choice(choices, message=message, **kwargs)

    def choice_dict(self, choices: Dict[str, Any], message: Optional[str] = None, **kwargs) -> "ChoiceDictPromptResponse":
        if message:
            message = self.format_message(message)
        return self.io.choice_dict(choices, message=message, **kwargs)

    def file_picker(self, path: str, pattern: Optional[str] = None, **kwargs) -> "FilePickerPromptResponse":
        return self.io.file_picker(path, pattern=pattern, **kwargs)

    def dir_picker(self, path: str, **kwargs) -> "DirPickerPromptResponse":
        return self.io.dir_picker(path, **kwargs)
