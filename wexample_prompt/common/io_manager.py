import shutil
import sys
import logging
from logging import Logger
from typing import Any, List, Optional, TextIO, Dict, Union
from pydantic import BaseModel, Field, ConfigDict, PrivateAttr
import requests

from wexample_prompt.mixins.with_indent import WithIndent
from wexample_prompt.themes.default.abstract_prompt_theme import AbstractPromptTheme
from wexample_prompt.themes.default.default_prompt_theme import DefaultPromptTheme
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.responses import BasePromptResponse
from wexample_prompt.common.error_context import ErrorContext
from wexample_prompt.responses.messages.error_prompt_response import ErrorPromptResponse
from wexample_prompt.responses.messages.warning_prompt_response import WarningPromptResponse
from wexample_prompt.responses.messages.success_prompt_response import SuccessPromptResponse
from wexample_prompt.responses.messages.info_prompt_response import InfoPromptResponse
from wexample_prompt.responses.messages.debug_prompt_response import DebugPromptResponse
from wexample_helpers_api.common.http_request_payload import HttpRequestPayload


class IoManager(BaseModel, WithIndent):
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
    _tty_width: int = PrivateAttr(default_factory=lambda: shutil.get_terminal_size().columns)
    _stdout: TextIO = PrivateAttr(default_factory=lambda: sys.stdout)
    _stdin: TextIO = PrivateAttr(default_factory=lambda: sys.stdin)

    def __init__(self, **data):
        super().__init__(**data)
        self._tty_width = shutil.get_terminal_size().columns
        self._stdout = sys.stdout
        self._stdin = sys.stdin
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

    def error(
        self,
        message: str,
        params: Optional[Dict[str, Any]] = None,
        fatal: bool = False,
        trace: bool = True,
        exit_code: int = 1
    ) -> ErrorPromptResponse:
        # Create context and response
        context = ErrorContext(
            fatal=fatal,
            trace=trace,
            params=params,
            exit_code=exit_code,
            indentation=self.log_indent
        )
        response = ErrorPromptResponse.create(message, context)
        
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
    ) -> WarningPromptResponse:
        context = ErrorContext(
            fatal=False,
            trace=trace,
            params=params,
            indentation=self.log_indent
        )
        response = WarningPromptResponse.create(message, context)
        
        # Log to file/system if configured
        if self._logger.handlers:
            self._logger.warning(message, extra={"params": params} if params else None)
        
        self.print_response(response)
        return response

    def success(self, message: str) -> SuccessPromptResponse:
        response = SuccessPromptResponse.create(message)
        
        # Log to file/system if configured
        if self._logger.handlers:
            self._logger.info(f"SUCCESS: {message}")
        
        self.print_response(response)
        return response

    def info(self, message: str) -> InfoPromptResponse:
        response = InfoPromptResponse.create(message)
        
        # Log to file/system if configured
        if self._logger.handlers:
            self._logger.info(message)
        
        self.print_response(response)
        return response

    def debug(self, message: str) -> DebugPromptResponse:
        response = DebugPromptResponse.create(message)
        
        # Log to file/system if configured
        if self._logger.handlers:
            self._logger.debug(message)
        
        self.print_response(response)
        return response

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

    def print_response_line(
        self,
        line: PromptResponseLine,
        response: BasePromptResponse
    ) -> None:
        line.print(self._stdout, response.context)

    def get_input(self, prompt: str = "") -> str:
        return input(prompt)

    def print(self, message: Any, **kwargs: Any) -> None:
        # Convert message to response if it's not already one
        if isinstance(message, BasePromptResponse):
            response = message
        else:
            response = InfoPromptResponse.create(str(message))
        
        self.print_response(response)

    def update_terminal_width(self) -> None:
        self._tty_width = shutil.get_terminal_size().columns

    @property
    def terminal_width(self) -> int:
        return self._tty_width

    def handle_api_response(
        self,
        response: Optional[requests.Response],
        request_context: HttpRequestPayload,
        exception: Optional[Exception] = None,
    ) -> Union[requests.Response, None]:
        # Format request details for logging
        request_details = {
            "url": request_context.url,
            "method": request_context.method,
        }
        if request_context.data:
            request_details["data"] = request_context.data
        if request_context.query_params:
            request_details["query_params"] = request_context.query_params

        # Handle request failure (no response)
        if not response:
            if exception:
                self.error(
                    f"Request failed: {str(exception)}",
                    params=request_details,
                    trace=True
                )
            return None

        # Log request details at debug level
        self.debug(
            f"{request_context.method} {request_context.url} "
            f"-> Status: {response.status_code}"
        )

        # Handle response based on status code
        if 200 <= response.status_code < 300:
            return response
        
        # Handle error response
        error_msg = f"HTTP {response.status_code}"
        try:
            error_data = response.json()
            if isinstance(error_data, dict):
                error_msg = error_data.get("message", error_data.get("error", error_msg))
        except (ValueError, AttributeError):
            if response.text:
                error_msg = response.text

        self.error(
            f"Request failed: {error_msg}",
            params=request_details,
            trace=bool(exception)
        )

        return None

