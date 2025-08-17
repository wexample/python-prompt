from abc import ABC
from typing import TYPE_CHECKING

from pydantic import BaseModel

from wexample_helpers.classes.mixin.has_snake_short_class_name_class_mixin import HasSnakeShortClassNameClassMixin
from wexample_prompt.common.prompt_context import PromptContext

if TYPE_CHECKING:
    pass


class AbstractPromptResponse(HasSnakeShortClassNameClassMixin, BaseModel, ABC):
    context: PromptContext = None

    def __init__(self, **data):
        if not "context" in data or not isinstance(data.get("context"), PromptContext):
            data["context"] = PromptContext()

        BaseModel.__init__(self, **data)

    def render(self) -> str:
        """Render the complete response."""
        return "TODO"
