from typing import List
from wexample_prompt.enums.text_style import TextStyle
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.formats import BaseFormat


class PromptResponse(BaseFormat):
    """A complete response that can contain multiple lines with different styles and layouts."""
    
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
