"""Properties response for displaying key-value pairs in a formatted box."""
from typing import Dict, Any, Optional

from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.enums.response_type import ResponseType
from wexample_prompt.responses.base_prompt_response import BasePromptResponse
from wexample_prompt.common.prompt_context import PromptContext


class PropertiesPromptResponse(BasePromptResponse):
    """Response for displaying properties in a box layout with borders."""

    properties: Dict[str, Any]
    title: Optional[str] = None
    nested_indent: int = 2

    @classmethod
    def create(
        cls,
        properties: Dict[str, Any],
        title: Optional[str] = None,
        nested_indent: int = 2,
        context: Optional[PromptContext] = None
    ) -> 'PropertiesPromptResponse':
        return cls(
            lines=[],  # Lines will be generated in render()
            response_type=ResponseType.PROPERTIES,
            properties=properties,
            title=title,
            nested_indent=nested_indent,
            context=context
        )

    def render(self) -> str:
        """Render the properties in a formatted box."""
        if not self.properties:
            return ""

        # Calculate the maximum width needed
        max_key_width = max(len(str(key)) for key in self.properties.keys())
        content_lines = self._format_properties(self.properties, max_key_width, self.nested_indent)
        
        # Calculate total width needed
        total_width = max(len(line) for line in content_lines) + 4  # Add padding
        
        lines = []
        
        # Add title if provided
        if self.title:
            title_padding = (total_width - len(self.title)) // 2
            title_line = PromptResponseLine(segments=[
                PromptResponseSegment(text="┌" + "─" * title_padding),
                PromptResponseSegment(text=f" {self.title} "),
                PromptResponseSegment(text="─" * (total_width - title_padding - len(self.title) - 2) + "┐")
            ])
            lines.append(title_line)
        else:
            # Top border
            lines.append(self._create_border_line(total_width, "┌", "┐"))
            
        # Add content lines
        for content in content_lines:
            padding = total_width - len(content) - 2
            lines.append(PromptResponseLine(segments=[
                PromptResponseSegment(text="│ "),
                PromptResponseSegment(text=content),
                PromptResponseSegment(text=" " * padding + "│")
            ]))
            
        # Bottom border
        lines.append(self._create_border_line(total_width, "└", "┘"))
        
        # Update lines and render using parent class
        self.lines = lines
        return super().render()

    @staticmethod
    def _format_properties(
        properties: Dict[str, Any],
        key_width: int,
        indent: int,
        current_indent: int = 0
    ) -> list[str]:
        """Format properties into lines, handling nested dictionaries.
        
        Args:
            properties: Dictionary of properties to format
            key_width: Width to align keys to
            indent: Number of spaces for each indentation level
            current_indent: Current indentation level
            
        Returns:
            List of formatted lines
        """
        lines = []
        indent_str = " " * current_indent
        
        for key, value in properties.items():
            if isinstance(value, dict):
                lines.append(f"{indent_str}{str(key)}:")
                lines.extend(PropertiesPromptResponse._format_properties(
                    value, key_width, indent, current_indent + indent
                ))
            else:
                key_str = str(key).ljust(key_width)
                lines.append(f"{indent_str}{key_str} : {str(value)}")
                
        return lines

    @staticmethod
    def _create_border_line(width: int, left: str = "├", right: str = "┤") -> PromptResponseLine:
        """Create a border line with the specified width and edge characters.
        
        Args:
            width: Total width of the line
            left: Left edge character
            right: Right edge character
            
        Returns:
            PromptResponseLine: A line for the border
        """
        return PromptResponseLine(segments=[
            PromptResponseSegment(text=f"{left}{'─' * (width - 2)}{right}")
        ])
