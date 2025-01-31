import logging
import shutil
import sys
from logging import Logger
from typing import Any, List, Optional, TextIO, Dict, Union, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr

from wexample_helpers.helpers.debug import debug_trace_and_die
from wexample_prompt.common.error_context import ErrorContext
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.mixins.with_indent import WithIndent
from wexample_prompt.protocol.io_handler_protocol import IoHandlerProtocol
from wexample_prompt.responses import BasePromptResponse
from wexample_prompt.themes.default.abstract_prompt_theme import AbstractPromptTheme
from wexample_prompt.themes.default.default_prompt_theme import DefaultPromptTheme

if TYPE_CHECKING:
    from wexample_prompt.responses.messages.error_prompt_response import ErrorPromptResponse
    from wexample_prompt.responses.messages.warning_prompt_response import WarningPromptResponse
    from wexample_prompt.responses.messages.success_prompt_response import SuccessPromptResponse
    from wexample_prompt.responses.messages.info_prompt_response import InfoPromptResponse
    from wexample_prompt.responses.messages.debug_prompt_response import DebugPromptResponse
    from wexample_prompt.responses.titles.title_prompt_response import TitlePromptResponse
    from wexample_prompt.responses.messages.log_prompt_response import LogPromptResponse
    from wexample_prompt.responses.titles.subtitle_prompt_response import SubtitlePromptResponse
    from wexample_prompt.responses.list_prompt_response import ListPromptResponse
    from wexample_prompt.responses.table_prompt_response import TablePromptResponse
    from wexample_prompt.responses.messages.failure_prompt_response import FailurePromptResponse
    from wexample_prompt.responses.messages.task_prompt_response import TaskPromptResponse
    from wexample_prompt.responses.tree_prompt_response import TreePromptResponse
    from wexample_prompt.responses.properties_prompt_response import PropertiesPromptResponse
    from wexample_prompt.responses.suggestions_prompt_response import SuggestionsPromptResponse
    from wexample_prompt.responses.progress_prompt_response import ProgressPromptResponse
    from wexample_prompt.responses.multiple_prompt_response import MultiplePromptResponse
    from wexample_prompt.responses.interactive.choice_prompt_response import ChoicePromptResponse
    from wexample_prompt.responses.interactive.choice_dict_prompt_response import ChoiceDictPromptResponse
    from wexample_prompt.responses.interactive.file_picker_prompt_response import FilePickerPromptResponse
    from wexample_prompt.responses.interactive.dir_picker_prompt_response import DirPickerPromptResponse


class IoManager(BaseModel, WithIndent, IoHandlerProtocol):
    """Manager for handling I/O operations in the prompt system."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    theme: AbstractPromptTheme = Field(
        default_factory=DefaultPromptTheme,
        description="Theme for customizing colors and styles"
    )
    log_level: int = Field(
        default=logging.INFO,
        description="Minimum log level for file logging"
    )
    log_file: Optional[str] = Field(
        default=None,
        description="Path to log file. If None, file logging is disabled"
    )

    _logger: Logger = PrivateAttr()
    _instance_count: int = PrivateAttr(default=0)
    _tty_width: int = PrivateAttr(default_factory=lambda: shutil.get_terminal_size().columns)
    _stdout: TextIO = PrivateAttr(default_factory=lambda: sys.stdout)
    _stdin: TextIO = PrivateAttr(default_factory=lambda: sys.stdin)
    _last_context: Optional[str] = PrivateAttr(default=None)

    def __init__(self, **data):
        super().__init__(**data)
        self._tty_width = shutil.get_terminal_size().columns
        self._stdout = sys.stdout
        self._stdin = sys.stdin
        self._last_context = None
        self._setup_logger()

    def _setup_logger(self) -> None:
        """Configure the Python logger with proper formatting and handlers."""
        self._logger = logging.getLogger("prompt")
        self._logger.setLevel(self.log_level)

        # Clear any existing handlers
        self._logger.handlers.clear()

        # Only add file handler if log_file is specified
        if self.log_file:
            file_handler = logging.FileHandler(self.log_file)
            file_handler.setFormatter(
                logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            )
            self._logger.addHandler(file_handler)

    def log_raw(self, level: int, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """
        Log a message directly to the logger without UI formatting.
        Useful for internal logging or passing data between processes.
        """
        if self._logger.handlers:
            self._logger.log(level, message, extra=extra)

    def print_responses(self, responses: List[BasePromptResponse]) -> None:
        for response in responses:
            self.print_response(response)

    def print_response(self, response: BasePromptResponse) -> None:
        """Print a response using its own context."""
        # If response has a context but no indentation, set it
        if response.context.indentation == 0 and self.log_indent > 0:
            response.context.indentation = self.log_indent

        response.print(output=self._stdout)

    def get_input(self, prompt: str = "") -> str:
        return input(prompt)

    def print(self, message: Any, **kwargs: Any) -> None:
        # Convert message to response if it's not already one
        if isinstance(message, BasePromptResponse):
            response = message
        else:
            response = InfoPromptResponse.create_info(str(message))

        self.print_response(response)

    def update_terminal_width(self) -> None:
        self._tty_width = shutil.get_terminal_size().columns

    @property
    def terminal_width(self) -> int:
        return self._tty_width

    def error(
        self,
        message: Optional[Union[str, Exception]] = None,
        params: Optional[Dict[str, Any]] = None,
        exception=None,
        fatal: bool = True,
    ) -> "ErrorPromptResponse":
        from wexample_prompt.responses.messages.error_prompt_response import ErrorPromptResponse

        # Create context and response
        context = ErrorContext(
            fatal=fatal,
            params=params,
            indentation=self.log_indent,
            terminal_width=self.terminal_width,
        )
        response = ErrorPromptResponse.create_error(
            message=message,
            context=context,
            exception=exception
        )

        # Log to file/system if configured
        if self._logger.handlers:
            self._logger.error(message, extra={"params": params} if params else None)

        # Display formatted message
        self.print_response(response)
        return response

    def warning(
        self,
        message: str,
        params: Optional[Dict[str, Any]] = None,
        trace: bool = False
    ) -> "WarningPromptResponse":
        from wexample_prompt.responses.messages.warning_prompt_response import WarningPromptResponse
        response = WarningPromptResponse.create_warning(
            message,
            ErrorContext(
                fatal=False,
                params=params,
                indentation=self.log_indent,
                terminal_width=self.terminal_width,
            )
        )

        # Log to file/system if configured
        if self._logger.handlers:
            self._logger.warning(message, extra={"params": params} if params else None)

        self.print_response(response)
        return response

    def _create_context(self):
        return PromptContext(
            indentation=self.log_indent,
            terminal_width=self.terminal_width
        )

    def success(self, message: str) -> "SuccessPromptResponse":
        from wexample_prompt.responses.messages.success_prompt_response import SuccessPromptResponse

        response = SuccessPromptResponse.create_success(
            message=message,
            context=self._create_context(),
        )

        # Log to file/system if configured
        if self._logger.handlers:
            self._logger.info(f"SUCCESS: {message}")

        self.print_response(response)
        return response

    def info(self, message: str) -> "InfoPromptResponse":
        from wexample_prompt.responses.messages.info_prompt_response import InfoPromptResponse

        response = InfoPromptResponse.create_info(
            message=message,
            context=self._create_context(),
        )

        # Log to file/system if configured
        if self._logger.handlers:
            self._logger.info(message)

        self.print_response(response)
        return response

    def debug(self, message: str) -> "DebugPromptResponse":
        from wexample_prompt.responses.messages.debug_prompt_response import DebugPromptResponse

        response = DebugPromptResponse.create_debug(
            message=message,
            context=self._create_context()
        )

        # Log to file/system if configured
        if self._logger.handlers:
            self._logger.debug(message)

        self.print_response(response)
        return response

    def title(self, message: str, **kwargs) -> "TitlePromptResponse":
        from wexample_prompt.responses.titles.title_prompt_response import TitlePromptResponse

        response = TitlePromptResponse.create_title(
            text=message,
            context=self._create_context(),
        )

        # Log to file/system if configured
        if self._logger.handlers:
            self._logger.debug(message)

        self.print_response(response)
        return response

    def subtitle(self, message: str, **kwargs) -> "SubtitlePromptResponse":
        from wexample_prompt.responses.titles.subtitle_prompt_response import SubtitlePromptResponse

        response = SubtitlePromptResponse.create_subtitle(
            text=message,
            context=self._create_context(),
        )

        # Log to file/system if configured
        if self._logger.handlers:
            self._logger.debug(message)

        self.print_response(response)
        return response

    def log(self, message: str, **kwargs) -> "LogPromptResponse":
        from wexample_prompt.responses.messages.log_prompt_response import LogPromptResponse

        response = LogPromptResponse.create_log(
            message=message,
            context=self._create_context(),
        )

        # Log to file/system if configured
        if self._logger.handlers:
            self._logger.debug(message)

        self.print_response(response)
        return response

    def debug(self, message: str, **kwargs) -> "DebugPromptResponse":
        from wexample_prompt.responses.messages.debug_prompt_response import DebugPromptResponse

        response = DebugPromptResponse.create_debug(
            message=message,
            context=self._create_context(),
        )

        if self._logger.handlers:
            self._logger.debug(message)

        self.print_response(response)
        return response

    def failure(self, message: str, **kwargs) -> "FailurePromptResponse":
        from wexample_prompt.responses.messages.failure_prompt_response import FailurePromptResponse

        response = FailurePromptResponse.create_failure(
            message=message,
            context=self._create_context(),
        )

        if self._logger.handlers:
            self._logger.error(message)

        self.print_response(response)
        return response

    def success(self, message: str, **kwargs) -> "SuccessPromptResponse":
        from wexample_prompt.responses.messages.success_prompt_response import SuccessPromptResponse

        response = SuccessPromptResponse.create_success(
            message=message,
            context=self._create_context(),
        )

        if self._logger.handlers:
            self._logger.info(message)

        self.print_response(response)
        return response

    def task(self, message: str, **kwargs) -> "TaskPromptResponse":
        from wexample_prompt.responses.messages.task_prompt_response import TaskPromptResponse

        response = TaskPromptResponse.create_task(
            message=message,
            context=self._create_context(),
        )

        if self._logger.handlers:
            self._logger.info(message)

        self.print_response(response)
        return response

    def warning(self, message: str, **kwargs) -> "WarningPromptResponse":
        from wexample_prompt.responses.messages.warning_prompt_response import WarningPromptResponse

        response = WarningPromptResponse.create_warning(
            message=message,
            context=self._create_context(),
        )

        if self._logger.handlers:
            self._logger.warning(message)

        self.print_response(response)
        return response

    def tree(self, data: Dict[str, Any], **kwargs) -> "TreePromptResponse":
        from wexample_prompt.responses.tree_prompt_response import TreePromptResponse

        response = TreePromptResponse.create_tree(
            data=data,
            context=self._create_context(),
        )

        self.print_response(response)
        return response

    def properties(self, properties: Dict[str, Any], **kwargs) -> "PropertiesPromptResponse":
        from wexample_prompt.responses.properties_prompt_response import PropertiesPromptResponse

        response = PropertiesPromptResponse.create_properties(
            properties=properties,
            context=self._create_context(),
        )

        self.print_response(response)
        return response

    def suggestions(self, suggestions: List[str], **kwargs) -> "SuggestionsPromptResponse":
        from wexample_prompt.responses.suggestions_prompt_response import SuggestionsPromptResponse

        response = SuggestionsPromptResponse.create_suggestions(
            suggestions=suggestions,
            context=self._create_context(),
        )

        self.print_response(response)
        return response

    def progress(self, total: int, message: Optional[str] = None, **kwargs) -> "ProgressPromptResponse":
        from wexample_prompt.responses.progress_prompt_response import ProgressPromptResponse

        response = ProgressPromptResponse.create_progress(
            total=total,
            message=message,
            context=self._create_context(),
        )

        self.print_response(response)
        return response

    def multiple(self, responses: List[Any], **kwargs) -> "MultiplePromptResponse":
        from wexample_prompt.responses.multiple_prompt_response import MultiplePromptResponse

        response = MultiplePromptResponse.create_multiple(
            responses=responses,
            context=self._create_context(),
        )

        self.print_response(response)
        return response

    def choice(self, choices: List[str], message: Optional[str] = None, **kwargs) -> "ChoicePromptResponse":
        from wexample_prompt.responses.interactive.choice_prompt_response import ChoicePromptResponse

        response = ChoicePromptResponse.create_choice(
            choices=choices,
            message=message,
            context=self._create_context(),
        )

        self.print_response(response)
        return response

    def choice_dict(self, choices: Dict[str, Any], message: Optional[str] = None, **kwargs) -> "ChoiceDictPromptResponse":
        from wexample_prompt.responses.interactive.choice_dict_prompt_response import ChoiceDictPromptResponse

        response = ChoiceDictPromptResponse.create_choice_dict(
            choices=choices,
            message=message,
            context=self._create_context(),
        )

        self.print_response(response)
        return response

    def file_picker(self, path: str, pattern: Optional[str] = None, **kwargs) -> "FilePickerPromptResponse":
        from wexample_prompt.responses.interactive.file_picker_prompt_response import FilePickerPromptResponse

        response = FilePickerPromptResponse.create_file_picker(
            path=path,
            pattern=pattern,
            context=self._create_context(),
        )

        self.print_response(response)
        return response

    def dir_picker(self, path: str, **kwargs) -> "DirPickerPromptResponse":
        from wexample_prompt.responses.interactive.dir_picker_prompt_response import DirPickerPromptResponse

        response = DirPickerPromptResponse.create_dir_picker(
            path=path,
            context=self._create_context(),
        )

        self.print_response(response)
        return response
