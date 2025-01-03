"""Input/Output manager for the prompt system."""
import shutil
import sys
from typing import Any, List, Optional, TextIO, Union

from pydantic import BaseModel, Field, PrivateAttr

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.mixins.with_indent import WithIndent
from wexample_prompt.themes.default.abstract_prompt_theme import AbstractPromptTheme
from wexample_prompt.themes.default.default_prompt_theme import DefaultPromptTheme
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.responses import BasePromptResponse


class IOManager(BaseModel, WithIndent):
    """Manages input/output operations for the prompt system."""

    theme: AbstractPromptTheme = Field(
        default_factory=DefaultPromptTheme,
        description="Theme for customizing colors and styles"
    )
    
    # Private attributes
    _tty_width: int = PrivateAttr(default_factory=lambda: shutil.get_terminal_size().columns)
    _stdout: TextIO = PrivateAttr(default=sys.stdout)
    _stdin: TextIO = PrivateAttr(default=sys.stdin)
    
    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True
    
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
        # Get color based on line type or response type
        color = self.theme.get_color(line.line_type or response.message_type)
        
        # Build the line with indentation and color
        rendered_line = line.render()
        if rendered_line:
            formatted_line = f"{self.build_indent()}{color}{rendered_line}{TerminalColor.RESET.value}"
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
