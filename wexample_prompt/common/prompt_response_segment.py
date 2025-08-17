from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, Field
from wexample_prompt.enums.terminal_color import TerminalColor

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext


class PromptResponseSegment(BaseModel):
    """A segment of text with optional styling."""
    text: str = Field(
        description="The content of the segment"
    )
    color: Optional[TerminalColor] = Field(
        default=None,
        description="The color to apply to segment on rendering, if allowed by context"
    )

    def render(self, context: "PromptContext") -> str:
        """Render the segment with its styles."""
        result = self.text

        if self.color and context.colorized:
            from wexample_prompt.common.color_manager import ColorManager
            result = ColorManager.colorize(result, self.color)

        return result
