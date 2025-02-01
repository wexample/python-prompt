import logging
import shutil
import sys
from logging import Logger
from typing import Any, List, Optional, TextIO, Type, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.mixins.response.manager.messages.debug_prompt_response_manager_mixin import \
    DebugPromptResponseManagerMixin
from wexample_prompt.mixins.response.manager.messages.log_prompt_response_manager_mixin import \
    LogPromptResponseManagerMixin
from wexample_prompt.mixins.response.manager.messages.info_prompt_response_manager_mixin import \
    InfoPromptResponseManagerMixin
from wexample_prompt.mixins.response.manager.titles.title_prompt_response_manager_mixin import \
    TitlePromptResponseManagerMixin
from wexample_prompt.mixins.response.manager.titles.subtitle_prompt_response_manager_mixin import \
    SubtitlePromptResponseManagerMixin
from wexample_prompt.mixins.with_indent import WithIndent
from wexample_prompt.protocol.io_handler_protocol import IoHandlerProtocol
from wexample_prompt.responses import BasePromptResponse
from wexample_prompt.themes.default.abstract_prompt_theme import AbstractPromptTheme
from wexample_prompt.themes.default.default_prompt_theme import DefaultPromptTheme

if TYPE_CHECKING:
    from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse


class IoManager(
    BaseModel,
    WithIndent,
    TitlePromptResponseManagerMixin,
    SubtitlePromptResponseManagerMixin,
    LogPromptResponseManagerMixin,
    InfoPromptResponseManagerMixin,
    DebugPromptResponseManagerMixin,
):
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
    terminal_width: int = Field(
        default_factory=lambda: shutil.get_terminal_size().columns,
        description="Width of the terminal"
    )
    _logger: Optional[Logger] = PrivateAttr(default=None)
    _log_file_handler: Optional[TextIO] = PrivateAttr(default=None)
    _instance_count: int = PrivateAttr(default=0)
    _tty_width: int = PrivateAttr(default_factory=lambda: shutil.get_terminal_size().columns)
    _stdout: TextIO = PrivateAttr(default_factory=lambda: sys.stdout)
    _stdin: TextIO = PrivateAttr(default_factory=lambda: sys.stdin)
    _last_context: Optional[str] = PrivateAttr(default=None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._tty_width = shutil.get_terminal_size().columns
        self._stdout = sys.stdout
        self._stdin = sys.stdin
        self._last_context = None
        self._setup_logger()

    def _setup_logger(self):
        """Set up logging configuration."""
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(self.log_level)
        
        # Clear any existing handlers
        self._logger.handlers.clear()
        
        if self.log_file:
            self._log_file_handler = logging.FileHandler(self.log_file)
            self._logger.addHandler(self._log_file_handler)

    def __del__(self):
        """Clean up resources."""
        if self._log_file_handler:
            self._log_file_handler.close()

    def get_response_types(self) -> List[Type["AbstractPromptResponse"]]:
        from wexample_prompt.responses.interactive.choice_dict_prompt_response import ChoiceDictPromptResponse
        from wexample_prompt.responses.interactive.choice_prompt_response import ChoicePromptResponse
        from wexample_prompt.responses.interactive.dir_picker_prompt_response import DirPickerPromptResponse
        from wexample_prompt.responses.interactive.file_picker_prompt_response import FilePickerPromptResponse
        from wexample_prompt.responses.list_prompt_response import ListPromptResponse
        from wexample_prompt.responses.messages.debug_prompt_response import DebugPromptResponse
        from wexample_prompt.responses.messages.error_prompt_response import ErrorPromptResponse
        from wexample_prompt.responses.messages.failure_prompt_response import FailurePromptResponse
        from wexample_prompt.responses.messages.info_prompt_response import InfoPromptResponse
        from wexample_prompt.responses.messages.log_prompt_response import LogPromptResponse
        from wexample_prompt.responses.messages.success_prompt_response import SuccessPromptResponse
        from wexample_prompt.responses.messages.task_prompt_response import TaskPromptResponse
        from wexample_prompt.responses.messages.warning_prompt_response import WarningPromptResponse
        from wexample_prompt.responses.multiple_prompt_response import MultiplePromptResponse
        from wexample_prompt.responses.progress_prompt_response import ProgressPromptResponse
        from wexample_prompt.responses.properties_prompt_response import PropertiesPromptResponse
        from wexample_prompt.responses.suggestions_prompt_response import SuggestionsPromptResponse
        from wexample_prompt.responses.table_prompt_response import TablePromptResponse
        from wexample_prompt.responses.titles.subtitle_prompt_response import SubtitlePromptResponse
        from wexample_prompt.responses.titles.title_prompt_response import TitlePromptResponse
        from wexample_prompt.responses.tree_prompt_response import TreePromptResponse

        return [
            ChoiceDictPromptResponse,
            ChoicePromptResponse,
            DirPickerPromptResponse,
            FilePickerPromptResponse,
            ListPromptResponse,
            DebugPromptResponse,
            ErrorPromptResponse,
            FailurePromptResponse,
            InfoPromptResponse,
            LogPromptResponse,
            SuccessPromptResponse,
            TaskPromptResponse,
            WarningPromptResponse,
            MultiplePromptResponse,
            ProgressPromptResponse,
            PropertiesPromptResponse,
            SuggestionsPromptResponse,
            TablePromptResponse,
            SubtitlePromptResponse,
            TitlePromptResponse,
            TreePromptResponse
        ]

    def _create_context(self) -> PromptContext:
        """Create a context with current indentation and terminal width."""
        return PromptContext(
            indentation=self.log_indent,
            terminal_width=self.terminal_width,
        )

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
            from wexample_prompt.responses.messages.info_prompt_response import InfoPromptResponse
            response = InfoPromptResponse.create_info(str(message))

        self.print_response(response)

    def update_terminal_width(self) -> None:
        self._tty_width = shutil.get_terminal_size().columns
