from typing import TYPE_CHECKING, List

from pydantic import Field
from wexample_prompt.common.prompt_response_line import PromptResponseLine

from wexample_helpers.classes.extended_base_model import ExtendedBaseModel
from wexample_helpers.classes.mixin.has_snake_short_class_name_class_mixin import HasSnakeShortClassNameClassMixin
from wexample_prompt.common.prompt_context import PromptContext

if TYPE_CHECKING:
    pass


class AbstractPromptResponse(HasSnakeShortClassNameClassMixin, ExtendedBaseModel):
    """Abstract base class for all prompt responses."""
    lines: List[PromptResponseLine] = Field(
        default_factory=list,
        description="The list of lines of the response content",
    )
    context: PromptContext = Field(
        default_factory=PromptContext,
        description="Execution context for prompt rendering",
    )

    def __init__(self, **kwargs):
        if not "context" in kwargs or not isinstance(kwargs.get("context"), PromptContext):
            kwargs["context"] = PromptContext()

        ExtendedBaseModel.__init__(self, **kwargs)

    def render(self) -> str:
        """Render the complete response."""
        rendered_lines = []

        for line in self.lines:
            rendered = line.render(self.context)
            rendered_lines.append(rendered)

        return "\n".join(rendered_lines)
