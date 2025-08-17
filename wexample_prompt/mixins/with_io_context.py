from typing import Optional

from pydantic import Field

from wexample_prompt.common.prompt_context import PromptContext


class WithIoContext:
    parent_io_context: Optional["PromptContext"] = Field(
        default=None,
        description="Get the io context of the parent class, used to propagate context data to current prompt level"
    )
    _io_context_colorized: Optional[bool] = None
    _io_context: "PromptContext"

    def __init__(
            self,
            parent_io_context: "PromptContext",
            **kwargs
    ):
        self._init_io_context(parent_io_context=parent_io_context)

    def _init_io_context(self, parent_io_context: "PromptContext"):
        self._io_context = PromptContext(
            parent_context=parent_io_context,
            indentation=self.get_io_context_indentation(),
            indentation_character=self.get_io_context_indentation_character(),
            colorized=self.get_io_context_colorized(),
        )

    def get_io_context_colorized(self) -> Optional[bool]:
        return None

    def get_io_context_indentation(self) -> Optional[int]:
        return None

    def get_io_context_indentation_character(self) -> Optional[str]:
        return None
