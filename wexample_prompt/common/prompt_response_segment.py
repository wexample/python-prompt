from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext


class PromptResponseSegment(BaseModel):
    """A segment of text with optional styling."""
    text: str = Field(
        description="The content of the segment"
    )

    def render(self, context: "PromptContext") -> str:
        """Render the segment with its styles."""
        result = self.text

        return result

