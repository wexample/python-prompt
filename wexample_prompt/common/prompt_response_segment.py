from typing import List, Optional
from pydantic import BaseModel

from wexample_prompt.enums.text_style import TextStyle


class PromptResponseSegment(BaseModel):
    """A segment of text with optional styling."""
    text: str
    styles: List[TextStyle] = []
    
    def combine(self, other: 'PromptResponseSegment') -> 'PromptResponseSegment':
        """Combine this segment with another, merging text and styles."""
        return PromptResponseSegment(
            text=self.text + other.text,
            styles=list(set(self.styles + other.styles))
        )
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PromptResponseSegment):
            return NotImplemented
        return self.text == other.text and set(self.styles) == set(other.styles)
    
    def apply_style(self, style: TextStyle) -> 'PromptResponseSegment':
        """Apply additional style to the segment."""
        return PromptResponseSegment(
            text=self.text,
            styles=list(set(self.styles + [style]))
        )
    
    def render(self, context: 'PromptContext') -> str:
        """Render the segment with its styles."""
        from wexample_prompt.common.prompt_context import PromptContext
        
        result = self.text
        if not context.should_use_color():
            return result
            
        # Apply styles in order
        for style in self.styles:
            result = self._apply_ansi_style(result, style)
            
        return result
    
    @staticmethod
    def _apply_ansi_style(text: str, style: TextStyle) -> str:
        """Apply ANSI style codes to text."""
        style_codes = {
            TextStyle.BOLD: "\033[1m",
            TextStyle.ITALIC: "\033[3m",
            TextStyle.UNDERLINE: "\033[4m",
            TextStyle.STRIKETHROUGH: "\033[9m",
            TextStyle.DIM: "\033[2m",
            TextStyle.REVERSE: "\033[7m",
            TextStyle.HIDDEN: "\033[8m",
        }
        return f"{style_codes[style]}{text}\033[0m"
