from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator

from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.enums.response_type import ResponseType
from wexample_prompt.enums.text_style import TextStyle
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.common.prompt_context import PromptContext


class PromptResponse(BaseModel):
    """A complete response that can contain multiple lines with different styles and layouts."""
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
    
    def append(self, other: 'PromptResponse') -> 'PromptResponse':
        """Combine this response with another."""
        return PromptResponse(
            lines=self.lines + other.lines,
            response_type=self.response_type,
            metadata={**self.metadata, **other.metadata},
            message_type=self.message_type
        )
    
    def wrap(self, styles: List[TextStyle]) -> 'PromptResponse':
        """Apply styles to all segments in all lines."""
        new_lines = []
        for line in self.lines:
            new_segments = [
                PromptResponseSegment(
                    text=segment.text,
                    styles=list(set(segment.styles + styles))
                )
                for segment in line.segments
            ]
            new_lines.append(PromptResponseLine(
                segments=new_segments,
                line_type=line.line_type,
                indent_level=line.indent_level,
                layout=line.layout
            ))
        return PromptResponse(
            lines=new_lines,
            response_type=self.response_type,
            metadata=self.metadata,
            message_type=self.message_type
        )
    
    @classmethod
    def table(cls, data: List[List[Any]], headers: Optional[List[str]] = None) -> 'PromptResponse':
        """Create a table response."""
        if not data:
            return cls(lines=[], response_type=ResponseType.TABLE)
            
        if headers:
            data.insert(0, headers)
            
        # Calculate column widths
        col_widths = [max(len(str(cell)) for cell in col) for col in zip(*data)]
        
        lines = []
        for row_idx, row in enumerate(data):
            segments = []
            for col_idx, (cell, width) in enumerate(zip(row, col_widths)):
                text = str(cell).ljust(width)
                if col_idx < len(row) - 1:
                    text += " | "
                segments.append(PromptResponseSegment(text=text))
            
            line = PromptResponseLine(segments=segments)
            lines.append(line)
            
            # Add separator after headers
            if headers and row_idx == 0:
                separator = PromptResponseLine(segments=[
                    PromptResponseSegment(text="-" * (sum(col_widths) + 3 * (len(col_widths) - 1)))
                ])
                lines.append(separator)
                
        return cls(lines=lines, response_type=ResponseType.TABLE)
    
    @classmethod
    def list(cls, items: List[str], bullet: str = "•") -> 'PromptResponse':
        """Create a list response."""
        lines = []
        for item in items:
            segments = [
                PromptResponseSegment(text=f"{bullet} "),
                PromptResponseSegment(text=str(item))
            ]
            lines.append(PromptResponseLine(segments=segments))
        return cls(lines=lines, response_type=ResponseType.LIST)
    
    @classmethod
    def tree(cls, data: Dict[str, Any], indent: int = 0) -> 'PromptResponse':
        """Create a tree response."""
        lines = []
        items = list(data.items())
        
        for idx, (key, value) in enumerate(items):
            is_last = idx == len(items) - 1
            prefix = "└── " if is_last else "├── "
            
            segments = [PromptResponseSegment(text=prefix + str(key))]
            lines.append(PromptResponseLine(
                segments=segments,
                indent_level=indent
            ))
            
            if isinstance(value, dict):
                # For dictionary values, add a new subtree
                subtree = cls.tree(value, indent + 1)
                lines.extend(subtree.lines)
            else:
                # For leaf nodes, use the same tree characters
                value_prefix = "└── " if True else "├── "  # Always last for leaf
                segments = [PromptResponseSegment(text=value_prefix + str(value))]
                lines.append(PromptResponseLine(
                    segments=segments,
                    indent_level=indent + 1
                ))
                
        return cls(lines=lines, response_type=ResponseType.TREE)
    
    @classmethod
    def progress(cls, total: int, current: int) -> 'PromptResponse':
        """Create a progress bar response."""
        percentage = min(100, int(100 * current / total))
        width = 50
        filled = int(width * current / total)
        
        bar = "[" + "=" * filled + " " * (width - filled) + "]"
        text = f"{bar} {percentage}%"
        
        return cls(
            lines=[PromptResponseLine(segments=[PromptResponseSegment(text=text)])],
            response_type=ResponseType.PROGRESS,
            metadata={"total": total, "current": current}
        )
