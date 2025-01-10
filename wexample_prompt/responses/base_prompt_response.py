from typing import List, Dict, Any, TextIO
import sys
from pydantic import Field

from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.enums.response_type import ResponseType
from wexample_prompt.common.prompt_response_line import PromptResponseLine
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
        
    def print(
        self,
        output: TextIO = sys.stdout,
        end: str = "\n",
        flush: bool = True,
    ) -> None:
        """Print the response to the specified output.
        
        Args:
            output: Output stream to print to
            end: String to append after the message
            flush: Whether to flush the output
        """
        rendered = self.render()
        if rendered:
            print(rendered, file=output, end=end, flush=flush)

        # Exit if fatal
        if self.context.fatal:
            sys.exit(self.context.exit_code)
    
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
