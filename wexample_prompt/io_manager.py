import shutil
import sys
from typing import Any, List, Optional, TextIO, Dict
from pydantic import BaseModel, Field, ConfigDict, PrivateAttr

from wexample_prompt.mixins.with_indent import WithIndent
from wexample_prompt.themes.default.abstract_prompt_theme import AbstractPromptTheme
from wexample_prompt.themes.default.default_prompt_theme import DefaultPromptTheme
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.responses import BasePromptResponse
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.common.error_context import ErrorContext
from wexample_prompt.responses.messages.error_prompt_response import ErrorPromptResponse
from wexample_prompt.responses.messages.warning_prompt_response import WarningPromptResponse
from wexample_prompt.responses.messages.success_prompt_response import SuccessPromptResponse
from wexample_prompt.responses.messages.info_prompt_response import InfoPromptResponse
from wexample_prompt.responses.messages.debug_prompt_response import DebugPromptResponse
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment


class IOManager(BaseModel, WithIndent):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    theme: AbstractPromptTheme = Field(
        default_factory=DefaultPromptTheme,
        description="Theme for customizing colors and styles"
    )
    
    _tty_width: int = PrivateAttr(default_factory=lambda: shutil.get_terminal_size().columns)
    _stdout: TextIO = PrivateAttr(default_factory=lambda: sys.stdout)
    _stdin: TextIO = PrivateAttr(default_factory=lambda: sys.stdin)
    
    def __init__(self, **data):
        super().__init__(**data)
        self._tty_width = shutil.get_terminal_size().columns
        self._stdout = sys.stdout
        self._stdin = sys.stdin
    
    def error(
        self,
        message: str,
        params: Optional[Dict[str, Any]] = None,
        fatal: bool = False,
        trace: bool = True,
        exit_code: int = 1
    ) -> ErrorPromptResponse:
        context = ErrorContext(
            fatal=fatal,
            trace=trace,
            params=params,
            exit_code=exit_code
        )
        response = ErrorPromptResponse.create(message, context)
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
            params=params
        )
        response = WarningPromptResponse.create(message, context)
        self.print_response(response)
        return response
    
    def success(self, message: str) -> SuccessPromptResponse:
        response = SuccessPromptResponse.create(message)
        self.print_response(response)
        return response
    
    def info(self, message: str) -> InfoPromptResponse:
        response = InfoPromptResponse.create(message)
        self.print_response(response)
        return response
    
    def debug(self, message: str) -> DebugPromptResponse:
        response = DebugPromptResponse.create(message)
        self.print_response(response)
        return response
    
    def print_responses(self, responses: List[BasePromptResponse]) -> None:
        for response in responses:
            self.print_response(response)
    
    def print_response(self, response: BasePromptResponse) -> None:
        # Create context with current theme, terminal width, and indentation
        context = PromptContext(
            theme=self.theme,
            terminal_width=self._tty_width,
            indentation=self.log_indent
        )
        
        # Use response's print function
        response.print(output=self._stdout, context=context)
    
    def print_response_line(
        self,
        line: PromptResponseLine,
        response: BasePromptResponse
    ) -> None:
        # Create a single-line response and print it
        temp_response = BasePromptResponse(
            lines=[line],
            response_type=response.response_type,
            message_type=response.message_type
        )
        self.print_response(temp_response)

    def get_input(self, prompt: str = "") -> str:
        return input(prompt)
    
    def print(self, message: Any, **kwargs: Any) -> None:
        # Convert message to response if it's not already one
        if isinstance(message, BasePromptResponse):
            self.print_response(message)
        else:
            # Create a simple response and print it
            response = BasePromptResponse(
                lines=[PromptResponseLine(segments=[
                    PromptResponseSegment(text=str(message))
                ])]
            )
            self.print_response(response)

    def update_terminal_width(self) -> None:
        self._tty_width = shutil.get_terminal_size().columns
    
    @property
    def terminal_width(self) -> int:
        return self._tty_width
