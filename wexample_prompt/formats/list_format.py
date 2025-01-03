from typing import List

from wexample_prompt.formats.base_format import BaseFormat
from wexample_prompt.enums.response_type import ResponseType
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment


class ListFormat(BaseFormat):
    """Format for displaying items in a bulleted list."""
    
    @classmethod
    def create(cls, items: List[str], bullet: str = "•") -> 'ListFormat':
        """Create a list format response."""
        lines = []
        for item in items:
            segments = [
                PromptResponseSegment(text=f"{bullet} "),
                PromptResponseSegment(text=str(item))
            ]
            lines.append(PromptResponseLine(segments=segments))
            
        return cls(lines=lines, response_type=ResponseType.LIST)
