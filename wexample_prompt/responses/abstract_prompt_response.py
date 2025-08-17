from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from wexample_helpers.classes.extended_base_model import ExtendedBaseModel
from wexample_helpers.classes.mixin.has_snake_short_class_name_class_mixin import HasSnakeShortClassNameClassMixin
from wexample_prompt.common.prompt_context import PromptContext

if TYPE_CHECKING:
    pass


class AbstractPromptResponse(HasSnakeShortClassNameClassMixin, ExtendedBaseModel):
    context: PromptContext = Field(
        default_factory=PromptContext,
        description="Execution context for prompt rendering",
    )

    def __init__(self, **data):
        if not "context" in data or not isinstance(data.get("context"), PromptContext):
            data["context"] = PromptContext()

        BaseModel.__init__(self, **data)

    def render(self) -> str:
        """Render the complete response."""
        return "TODO"
