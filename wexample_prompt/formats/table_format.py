from typing import List, Any, Optional

from wexample_prompt.formats.base_format import BaseFormat
from wexample_prompt.enums.response_type import ResponseType
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment


class TableFormat(BaseFormat):
    """Format for displaying data in a table layout."""
    
    @classmethod
    def create(cls, data: List[List[Any]], headers: Optional[List[str]] = None) -> 'TableFormat':
        """Create a table format response."""
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
