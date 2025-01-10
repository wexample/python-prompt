from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field

from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.enums.response_type import ResponseType
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.text_style import TextStyle

from wexample_prompt.enums.verbosity_level import VerbosityLevel


class AbstractPromptResponse(BaseModel, ABC):
    """Abstract base class for all prompt responses."""
    lines: List[PromptResponseLine]
    response_type: ResponseType = ResponseType.PLAIN
    metadata: Dict[str, Any] = Field(default_factory=dict)
    message_type: MessageType = MessageType.LOG
    context: Optional[PromptContext] = None
    verbosity_level: VerbosityLevel = Field(default=VerbosityLevel.DEFAULT)

    def __init__(self, **data):
        super().__init__(**data)
        # Create default context if none is provided
        if self.context is None:
            self.context = PromptContext()

    def render(self) -> str:
        """Render the complete response."""
        # Check if this message should be shown based on verbosity
        if not self.context.should_show_message(self.verbosity_level):
            return ""

        rendered_lines = []
        indent = self.context.get_indentation()
        for line in self.lines:
            rendered = line.render(self.context)
            if rendered:  # Only indent non-empty lines
                rendered = indent + rendered
            rendered_lines.append(rendered)

        # Format message with parameters if any
        return self.context.format_message(
            "\n".join(rendered_lines)
        )

    @classmethod
    @abstractmethod
    def create(cls: "AbstractPromptResponse", context: PromptContext = None, **kwargs) -> "AbstractPromptResponse":
        """
        Create a new instance of the response.
        
        Args:
            context: The context for this response
            **kwargs: Additional arguments specific to each response type
            
        Returns:
            A new instance of the response
        """
        pass
    
    def append(self, other: 'AbstractPromptResponse') -> 'AbstractPromptResponse':
        """Combine this response with another."""
        return self.__class__(
            lines=self.lines + other.lines,
            response_type=self.response_type,
            metadata={**self.metadata, **other.metadata},
            message_type=self.message_type,
            context=self.context
        )
    
    def wrap(self, styles: List[TextStyle]) -> 'AbstractPromptResponse':
        """Apply styles to all segments in all lines."""
        new_lines = []
        for line in self.lines:
            new_segments = [
                segment.with_styles(styles)
                for segment in line.segments
            ]
            new_lines.append(PromptResponseLine(
                segments=new_segments,
                line_type=line.line_type,
                indent_level=line.indent_level,
                layout=line.layout
            ))
        return self.__class__(
            lines=new_lines,
            response_type=self.response_type,
            metadata=self.metadata,
            message_type=self.message_type,
            context=self.context
        )
