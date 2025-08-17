"""Prompt response line implementation."""
from typing import List

from pydantic import BaseModel, Field

from wexample_prompt.common.prompt_response_segment import PromptResponseSegment


class PromptResponseLine(BaseModel):
    """A line of text composed of one or more segments with optional styling and layout."""

    segments: List[PromptResponseSegment] = Field(
        default_factory=list,
        description="List of text segments that constitute a line"
    )
