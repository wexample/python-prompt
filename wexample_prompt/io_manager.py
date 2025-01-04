"""Input/Output manager for the prompt system."""
import shutil
import sys
from typing import Any, List, Optional, TextIO, Union, Dict

from pydantic import BaseModel, Field, PrivateAttr

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

    theme: AbstractPromptTheme = Field(
        default_factory=DefaultPromptTheme,
        description="Theme for customizing colors and styles"
    )
    
    # Private attributes
    _tty_width: int = PrivateAttr()
    _stdout: TextIO = PrivateAttr()
    _stdin: TextIO = PrivateAttr()
    
    def __init__(self, **data):
        """Initialize IOManager with default values for private attributes."""
        super().__init__(**data)
        self._tty_width = shutil.get_terminal_size().columns
        self._stdout = sys.stdout
        self._stdin = sys.stdin
    
    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True
    
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
        for line in response.lines:
            self.print_response_line(line, response)
    
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
        # Get color based on line-type or response-type
        message_type = line.line_type or response.message_type
        color = ColorManager.MESSAGE_COLORS.get(message_type, TerminalColor.RESET)
        
        # Create context with current terminal width
        context = PromptContext(
            terminal_width=self._tty_width,
            is_tty=True
        )
        
        # Build the line with indentation and color
        rendered_line = line.render(context)
        if rendered_line:
            # Apply color only if supported
            if ColorManager.supports_color():
                formatted_line = f"{self.build_indent()}{color.value}{rendered_line}{TerminalColor.RESET.value}"
            else:
                formatted_line = f"{self.build_indent()}{rendered_line}"
            self.print(formatted_line)
    
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
        
        Args:
            message: Message to print
            **kwargs: Additional arguments passed to print()
        """
        print(message, file=self._stdout, **kwargs)
    
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
