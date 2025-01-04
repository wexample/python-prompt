"""Base class for all prompt responses."""
from typing import List, Dict, Any, Optional, TextIO
import sys
from pydantic import Field

from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.enums.response_type import ResponseType
from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse


class BasePromptResponse(AbstractPromptResponse):
    """Base class for all concrete prompt responses.
    
    This class inherits from AbstractPromptResponse and serves as the base
    for all concrete response implementations. It provides the basic functionality
    for rendering and manipulating prompt responses.
    """
    
    lines: List[PromptResponseLine]
    response_type: ResponseType = ResponseType.PLAIN
    metadata: Dict[str, Any] = Field(default_factory=dict)
    message_type: MessageType = MessageType.LOG
    verbosity_level: VerbosityLevel = Field(default=VerbosityLevel.DEFAULT)
    
    def render(self, context: Optional[PromptContext] = None) -> str:
        """Render the complete response."""
        if context is None:
            context = PromptContext()
            
        # Check if this message should be shown based on verbosity
        if not context.should_show_message(self.verbosity_level):
            return ""
            
        rendered_lines = []
        indent = context.get_indentation()
        for line in self.lines:
            rendered = line.render(context)
            if rendered:  # Only indent non-empty lines
                rendered = indent + rendered
            rendered_lines.append(rendered)
            
        return "\n".join(rendered_lines)
        
    def print(
        self,
        output: TextIO = sys.stdout,
        end: str = "\n",
        flush: bool = True,
        context: Optional[PromptContext] = None
    ) -> None:
        """Print the response to the specified output.
        
        This is the centralized print function for all responses. All output
        from any response type should go through this function.
        
        Args:
            output: Output stream to print to (default: sys.stdout)
            end: String to append after the output (default: newline)
            flush: Whether to flush the output stream (default: True)
            context: Optional context for rendering (default: None)
        """
        rendered = self.render(context)
        if rendered:  # Only print if there's content after verbosity check
            print(rendered, end=end, file=output, flush=flush)
    
    def append(self, other: 'BasePromptResponse') -> 'BasePromptResponse':
        """Combine this response with another."""
        return self.__class__(
            lines=self.lines + other.lines,
            response_type=self.response_type,
            metadata={**self.metadata, **other.metadata},
            message_type=self.message_type
        )

    @classmethod
    def create(cls, lines: List[PromptResponseLine]) -> 'BasePromptResponse':
        """Create a new response with the given lines."""
        return cls(lines=lines)
        
    @classmethod
    def create_from_text_lines(cls, text_lines: List[str]) -> 'BasePromptResponse':
        """Create a new response from simple text lines.
        
        This is a convenience method that converts a list of text strings into
        PromptResponseLine objects automatically.
        
        Args:
            text_lines: List of text strings to convert into response lines
            
        Returns:
            BasePromptResponse: A new response containing the text lines
        """
        from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
        
        lines = []
        for text in text_lines:
            # Create a simple segment with the text
            segment = PromptResponseSegment(text=text)
            # Create a line with just this segment
            line = PromptResponseLine(segments=[segment])
            lines.append(line)
            
        return cls.create(lines)
