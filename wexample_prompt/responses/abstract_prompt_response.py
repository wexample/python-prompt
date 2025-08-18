from abc import abstractmethod
from typing import TYPE_CHECKING, List, Optional, Type

from pydantic import Field

from wexample_helpers.classes.extended_base_model import ExtendedBaseModel
from wexample_helpers.classes.mixin.has_snake_short_class_name_class_mixin import HasSnakeShortClassNameClassMixin
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.common.prompt_response_line import PromptResponseLine

if TYPE_CHECKING:
    from wexample_prompt.example.abstract_response_example import AbstractResponseExample


class AbstractPromptResponse(HasSnakeShortClassNameClassMixin, ExtendedBaseModel):
    """Abstract base class for all prompt responses."""
    lines: List[PromptResponseLine] = Field(
        default_factory=list,
        description="The list of lines of the response content",
    )

    def __init__(self, **kwargs):
        ExtendedBaseModel.__init__(self, **kwargs)

    @classmethod
    @abstractmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        cls._raise_not_implemented_error()

    def render(self, context: Optional["PromptContext"] = None) -> str:
        """Render the complete response."""
        rendered_lines = []

        context = context or PromptContext()

        for line in self.lines:
            rendered = line.render(context)
            rendered_lines.append(rendered)

        return "\n".join(rendered_lines)
