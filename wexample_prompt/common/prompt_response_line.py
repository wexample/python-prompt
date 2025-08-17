"""Prompt response line implementation."""
from typing import List, Optional, TYPE_CHECKING

from pydantic import BaseModel, Field

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment

if TYPE_CHECKING:
    from wexample_prompt.enums.terminal_color import TerminalColor


class PromptResponseLine(BaseModel):
    """A line of text composed of one or more segments with optional styling and layout."""

    segments: List[PromptResponseSegment] = Field(
        default_factory=list,
        description="List of text segments that constitute a line"
    )

    @classmethod
    def create_from_string(cls, text: str, color: Optional["TerminalColor"] = None) -> "PromptResponseLine":
        """
            Create a line from a single text string.
        """
        return cls(
            segments=[
                PromptResponseSegment(
                    text=text,
                    color=color
                )
            ]
        )

    def render(self, context: PromptContext) -> str:
        """Render the line with all its segments.
        """

        # Render all segments
        rendered_segments = [seg.render(context) for seg in self.segments]
        result = "".join(rendered_segments)
        return result
