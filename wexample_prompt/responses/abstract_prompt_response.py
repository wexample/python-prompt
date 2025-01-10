from typing import List, Dict, Any, Optional, TypeVar, Generic
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field

from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.enums.response_type import ResponseType
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.text_style import TextStyle


T = TypeVar('T', bound='AbstractPromptResponse')
C = TypeVar('C', bound=PromptContext)

class AbstractPromptResponse(BaseModel, Generic[C], ABC):
    """Abstract base class for all prompt responses."""
    lines: List[PromptResponseLine]
    response_type: ResponseType = ResponseType.PLAIN
    metadata: Dict[str, Any] = Field(default_factory=dict)
    message_type: MessageType = MessageType.LOG
    context: Optional[C] = None
    
    def render(self) -> str:
        """Render the complete response."""
        rendered_lines = [line.render(self.context) for line in self.lines]
        return "\n".join(rendered_lines)
    
    @classmethod
    @abstractmethod
    def create(cls: type[T], context: C, **kwargs) -> T:
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
