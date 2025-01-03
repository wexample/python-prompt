from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.enums.response_type import ResponseType
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_context import PromptContext


class BaseFormat(BaseModel):
    """Base class for all prompt response formats."""
    lines: List[PromptResponseLine]
    response_type: ResponseType = ResponseType.PLAIN
    metadata: Dict[str, Any] = Field(default_factory=dict)
    message_type: MessageType = MessageType.LOG
    
    def render(self, context: Optional[PromptContext] = None) -> str:
        """Render the complete response."""
        if context is None:
            context = PromptContext()
            
        rendered_lines = [line.render(context) for line in self.lines]
        return "\n".join(rendered_lines)
    
    def append(self, other: 'BaseFormat') -> 'BaseFormat':
        """Combine this response with another."""
        return self.__class__(
            lines=self.lines + other.lines,
            response_type=self.response_type,
            metadata={**self.metadata, **other.metadata},
            message_type=self.message_type
        )
