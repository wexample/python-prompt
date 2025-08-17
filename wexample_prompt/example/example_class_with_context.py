from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel

from wexample_prompt.mixins.with_prompt_context import WithPromptContext

if TYPE_CHECKING:
    from wexample_prompt.common.io_manager import IoManager


class ExampleClassWithContext(WithPromptContext, BaseModel):

    def __init__(self, io: Optional["IoManager"] = None, **kwargs):
        BaseModel.__init__(self, **kwargs)
        WithPromptContext.__init__(self, io=io)

    def _format_context_prompt_message(self, message: str, indent: str) -> str:
        return f"{indent}[EXAMPLE|{self.__class__.__name__}]: {message}"
