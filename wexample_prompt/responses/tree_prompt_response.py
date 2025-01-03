from typing import Dict, Any

from wexample_prompt.responses.base_prompt_response import BasePromptResponse
from wexample_prompt.enums.response_type import ResponseType
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment


class TreePromptResponse(BasePromptResponse):
    """Response for displaying hierarchical data in a tree structure."""
    
    @classmethod
    def create(cls, data: Dict[str, Any]) -> 'TreePromptResponse':
        """Create a tree response."""
        lines = []
        cls._build_tree(data, "", lines)
        return cls(lines=lines, response_type=ResponseType.TREE)
    
    @classmethod
    def _build_tree(cls, data: Dict[str, Any], prefix: str, lines: list) -> None:
        """Recursively build tree structure."""
        items = list(data.items())
        for i, (key, value) in enumerate(items):
            is_last = i == len(items) - 1
            current_prefix = "└── " if is_last else "├── "
            
            # Add current node
            segments = [PromptResponseSegment(text=f"{prefix}{current_prefix}{key}")]
            lines.append(PromptResponseLine(segments=segments))
            
            # Process children
            if isinstance(value, dict):
                next_prefix = prefix + ("    " if is_last else "│   ")
                cls._build_tree(value, next_prefix, lines)
            elif value is not None:
                next_prefix = prefix + ("    " if is_last else "│   ")
                segments = [PromptResponseSegment(text=f"{next_prefix}└── {value}")]
                lines.append(PromptResponseLine(segments=segments))
