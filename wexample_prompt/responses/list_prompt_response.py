"""Response for displaying items in a bulleted list."""
from typing import List

from wexample_prompt.responses.base_prompt_response import BasePromptResponse
from wexample_prompt.enums.response_type import ResponseType
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment


class ListPromptResponse(BasePromptResponse):
    """Response for displaying items in a bulleted list."""
    
    @classmethod
    def create(cls, items: List[str], bullet: str = "•") -> 'ListPromptResponse':
        """Create a list response.
        
        Args:
            items: List of items to display
            bullet: Bullet character to use (default: •)
            
        Returns:
            ListPromptResponse: A new list response
        """
        lines = []
        for item in items:
            # Check if this is a sub-item by looking for leading spaces
            indent_level = 0
            content = item
            
            while content.startswith("  "):
                indent_level += 1
                content = content[2:]
                
            # Remove bullet if the content already has one
            if content.startswith(f"{bullet} "):
                content = content[2:]
                
            # Create line with proper indentation
            segments = [
                PromptResponseSegment(text="  " * indent_level + f"{bullet} "),
                PromptResponseSegment(text=content)
            ]
            lines.append(PromptResponseLine(segments=segments))
            
        return cls(lines=lines, response_type=ResponseType.LIST)
