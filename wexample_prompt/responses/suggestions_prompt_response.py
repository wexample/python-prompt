"""Response for displaying suggestions with optional descriptions."""
from typing import List, Optional

from wexample_prompt.responses.base_prompt_response import BasePromptResponse
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.common.color_manager import ColorManager
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.enums.text_style import TextStyle
from wexample_prompt.common.prompt_context import PromptContext


class SuggestionsPromptResponse(BasePromptResponse):
    """Response for displaying a list of suggestions with optional descriptions."""

    @classmethod
    def create(
        cls,
        message: str,
        suggestions: List[str],
        context: Optional[PromptContext] = None,
        **kwargs
    ) -> 'SuggestionsPromptResponse':
        lines = []
        
        # Add the message line with blue color and bold style
        lines.append(
            PromptResponseLine(segments=[
                PromptResponseSegment(
                    text=ColorManager.colorize(f"{message}:", TerminalColor.BLUE),
                    styles=[TextStyle.BOLD]
                )
            ])
        )
        
        # Add each suggestion with a modern arrow and styling
        for suggestion in suggestions:
            lines.append(
                PromptResponseLine(segments=[
                    # Arrow indicator with cyan color
                    PromptResponseSegment(
                        text=ColorManager.colorize("  → ", TerminalColor.CYAN),
                        styles=[TextStyle.BOLD]
                    ),
                    # Suggestion text
                    PromptResponseSegment(text=suggestion)
                ])
            )
            
        return cls(lines=lines, context=context)
