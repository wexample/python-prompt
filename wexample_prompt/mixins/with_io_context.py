from typing import Optional

from pydantic import Field

from wexample_prompt.common.prompt_context import PromptContext


class WithIoContext:
    parent_io_context: Optional["PromptContext"] = Field(
        default=None,
        description="Get the io context of the parent class, used to propagate context data to current prompt level"
    )
    _io_context: "PromptContext"

    def __init__(self, parent_io_context: "PromptContext", **kwargs):
        self._init_io_context(parent_io_context=parent_io_context)

    def _init_io_context(self, parent_io_context: "PromptContext"):
        self._io_context = PromptContext(
            indentation=parent_io_context.indentation + 1,
            indentation_character=parent_io_context.indentation_character,
            colorized=parent_io_context.colorized,
        )
