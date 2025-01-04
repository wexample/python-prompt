"""Input/Output manager for the prompt system."""
import shutil
import sys
from typing import Any, List, Optional, TextIO, Union, Dict

from pydantic import BaseModel, Field, ConfigDict, PrivateAttr

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.mixins.with_indent import WithIndent
from wexample_prompt.themes.default.abstract_prompt_theme import AbstractPromptTheme
from wexample_prompt.themes.default.default_prompt_theme import DefaultPromptTheme
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.responses import BasePromptResponse
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.common.color_manager import ColorManager
from wexample_prompt.common.error_context import ErrorContext
from wexample_prompt.responses.messages.error_prompt_response import ErrorPromptResponse
from wexample_prompt.responses.messages.warning_prompt_response import WarningPromptResponse
from wexample_prompt.responses.messages.success_prompt_response import SuccessPromptResponse
from wexample_prompt.responses.messages.info_prompt_response import InfoPromptResponse
from wexample_prompt.responses.messages.debug_prompt_response import DebugPromptResponse


class IOManager(BaseModel, WithIndent):
    """Manages input/output operations for the prompt system."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    theme: AbstractPromptTheme = Field(
        default_factory=DefaultPromptTheme,
        description="Theme for customizing colors and styles"
    )
    
    # Private attributes using PrivateAttr for true private fields
    _tty_width: int = PrivateAttr(default_factory=lambda: shutil.get_terminal_size().columns)
    _stdout: TextIO = PrivateAttr(default_factory=lambda: sys.stdout)
    _stdin: TextIO = PrivateAttr(default_factory=lambda: sys.stdin)
    
    def __init__(self, **data):
        """Initialize IOManager with default values for private attributes."""
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
        """Print an error message.
        
        Args:
            message: Error message text
            params: Optional parameters for message formatting
            fatal: If True, exit after printing
            trace: If True, include stack trace
            exit_code: Exit code to use if fatal is True
            
        Returns:
            ErrorPromptResponse instance
            
        Note:
            If fatal is True, this method will not return
        """
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
        """Print a warning message.
        
        Args:
            message: Warning message text
            params: Optional parameters for message formatting
            trace: If True, include stack trace
            
        Returns:
            WarningPromptResponse instance
        """
        context = ErrorContext(
            fatal=False,
            trace=trace,
            params=params
        )
        response = WarningPromptResponse.create(message, context)
        self.print_response(response)
        return response
    
    def success(self, message: str) -> SuccessPromptResponse:
        """Print a success message.
        
        Args:
            message: Success message text
            
        Returns:
            SuccessPromptResponse instance
        """
        response = SuccessPromptResponse.create(message)
        self.print_response(response)
        return response
    
    def info(self, message: str) -> InfoPromptResponse:
        """Print an info message.
        
        Args:
            message: Info message text
            
        Returns:
            InfoPromptResponse instance
        """
        response = InfoPromptResponse.create(message)
        self.print_response(response)
        return response
    
    def debug(self, message: str) -> DebugPromptResponse:
        """Print a debug message.
        
        Args:
            message: Debug message text
            
        Returns:
            DebugPromptResponse instance
        """
        response = DebugPromptResponse.create(message)
        self.print_response(response)
        return response
    
    def print_responses(self, responses: List[BasePromptResponse]) -> None:
        """Print multiple responses in sequence.
        
        Args:
            responses: List of responses to print
        """
        for response in responses:
            self.print_response(response)
    
    def print_response(self, response: BasePromptResponse) -> None:
        """Print a single response.
        
        Args:
            response: Response to print
        """
        # Create context with current theme, terminal width, and indentation
        context = PromptContext(
            theme=self.theme,
            terminal_width=self._tty_width,
            indentation=self._log_indent
        )
        
        # Use response's print function
        response.print(output=self._stdout, context=context)
    
    def print_response_line(
        self,
        line: PromptResponseLine,
        response: BasePromptResponse
    ) -> None:
        """Print a single line from a response.
        
        Args:
            line: Line to print
            response: Parent response containing the line
        """
        # Create a single-line response and print it
        temp_response = BasePromptResponse(
            lines=[line],
            response_type=response.response_type,
            message_type=response.message_type
        )
        self.print_response(temp_response)

    def get_input(self, prompt: str = "") -> str:
        """Get input from the user.
        
        Args:
            prompt: Optional prompt text to display
            
        Returns:
            User input string
        """
        return input(prompt)
    
    def print(self, message: Any, **kwargs: Any) -> None:
        """Print a message to stdout.
        
        This method is deprecated. Use print_response() instead.
        
        Args:
            message: Message to print
            **kwargs: Additional arguments passed to print()
        """
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
        """Update the stored terminal width."""
        self._tty_width = shutil.get_terminal_size().columns
    
    @property
    def terminal_width(self) -> int:
        """Get the current terminal width.
        
        Returns:
            Current terminal width in columns
        """
        return self._tty_width
