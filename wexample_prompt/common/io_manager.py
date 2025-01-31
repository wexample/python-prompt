import logging
import shutil
import sys
from logging import Logger
from typing import Any, List, Optional, TextIO, Dict, Union

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr

from wexample_helpers.helpers.debug import debug_trace_and_die
from wexample_prompt.common.error_context import ErrorContext
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.mixins.with_indent import WithIndent
from wexample_prompt.protocol.io_handler_protocol import IoHandlerProtocol
from wexample_prompt.responses import BasePromptResponse
from wexample_prompt.responses.titles.title_prompt_response import TitlePromptResponseIoManagerMixin
from wexample_prompt.responses.titles.subtitle_prompt_response import SubtitlePromptResponseIoManagerMixin
from wexample_prompt.responses.messages.log_prompt_response import LogPromptResponseIoManagerMixin
from wexample_prompt.themes.default.abstract_prompt_theme import AbstractPromptTheme
from wexample_prompt.themes.default.default_prompt_theme import DefaultPromptTheme


class IoManager(
    BaseModel,
    WithIndent,
    TitlePromptResponseIoManagerMixin,
    SubtitlePromptResponseIoManagerMixin,
    LogPromptResponseIoManagerMixin,
    IoHandlerProtocol
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

    @property
    def terminal_width(self) -> int:
        return self._tty_width
