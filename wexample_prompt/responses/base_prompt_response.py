from typing import List, Dict, Any, TextIO
import sys
from pydantic import Field

from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.enums.response_type import ResponseType
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse


class BasePromptResponse(AbstractPromptResponse):
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
        rendered = self.render()
        if rendered:
            print(rendered, file=output, end=end, flush=flush)

        # Exit if fatal
        if self.context.fatal:
            self._on_fatal()

    def _on_fatal(self):
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
    def create_from_text_lines(cls, text_lines: List[str]) -> 'BasePromptResponse':
        from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
        
        lines = []
        for text in text_lines:
            # Create a simple segment with the text
            segment = PromptResponseSegment(text=text)
            # Create a line with just this segment
            line = PromptResponseLine(segments=[segment])
            lines.append(line)
            
        return cls.create(lines)
