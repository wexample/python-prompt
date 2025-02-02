"""Response for displaying suggestions with optional descriptions."""
from typing import List, Optional

from wexample_prompt.responses.base_prompt_response import BasePromptResponse
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.common.color_manager import ColorManager
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.enums.text_style import TextStyle
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.enums.response_type import ResponseType


class SuggestionsPromptResponse(BasePromptResponse):
    """Response for displaying a list of suggestions with optional descriptions."""

    # Instance variables
    message: str
    suggestions: List[str]
    arrow_style: str = "→"

    @classmethod
    def create_suggestions(
        cls,
        message: str,
        suggestions: List[str],
        context: Optional[PromptContext] = None,
        verbosity: Optional[VerbosityLevel] = None,
        arrow_style: str = "→"
    ) -> 'SuggestionsPromptResponse':
        """Create a suggestions response.

        Args:
            message: The message to display above suggestions
            suggestions: List of suggestion strings to display
            context: Optional prompt context for formatting
            verbosity: Optional verbosity level for output detail
            arrow_style: Character to use as bullet point (default: →)

        Returns:
            SuggestionsPromptResponse instance
        """
        return cls(
            lines=[],  # Lines will be generated in render()
            response_type=ResponseType.SUGGESTIONS,
            message=message,
            suggestions=suggestions,
            arrow_style=arrow_style,
            context=context,
            verbosity_level=verbosity or VerbosityLevel.DEFAULT
        )

    def render(self) -> str:
        """Render the suggestions with styling."""
        lines = []
        
        # Add the message line with blue color and bold style
        lines.append(
            PromptResponseLine(segments=[
                PromptResponseSegment(
                    text=ColorManager.colorize(f"{self.message}:", TerminalColor.BLUE),
                    styles=[TextStyle.BOLD]
                )
            ])
        )
        
        # Add each suggestion with a modern arrow and styling
        for suggestion in self.suggestions:
            lines.append(
                PromptResponseLine(segments=[
                    # Arrow indicator with cyan color
                    PromptResponseSegment(
                        text=ColorManager.colorize(f"  {self.arrow_style} ", TerminalColor.CYAN),
                        styles=[TextStyle.BOLD]
                    ),
                    # Suggestion text
                    PromptResponseSegment(text=suggestion)
                ])
            )
            
        # Update lines and render using parent class
        self.lines = lines
        return super().render()
