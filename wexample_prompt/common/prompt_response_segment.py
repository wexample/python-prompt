from pydantic import BaseModel, Field


class PromptResponseSegment(BaseModel):
    """A segment of text with optional styling."""
    text: str = Field(
        description="The content of the segment"
    )
