from abc import abstractmethod
from typing import TYPE_CHECKING, List, Optional, Type

from pydantic import Field

from wexample_helpers.classes.extended_base_model import ExtendedBaseModel
from wexample_helpers.classes.mixin.has_snake_short_class_name_class_mixin import HasSnakeShortClassNameClassMixin
from wexample_helpers.const.types import Kwargs
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.enums.verbosity_level import VerbosityLevel

if TYPE_CHECKING:
    from wexample_prompt.example.abstract_response_example import AbstractResponseExample


class AbstractPromptResponse(HasSnakeShortClassNameClassMixin, ExtendedBaseModel):
    """Abstract base class for all prompt responses."""
    lines: List[PromptResponseLine] = Field(
        default_factory=list,
        description="The list of lines of the response content",
    )
    verbosity: Optional[VerbosityLevel] = Field(
        default=VerbosityLevel.DEFAULT,
        description="The context verbosity, saying which response to render or not"
    )

    def __init__(self, **kwargs):
        ExtendedBaseModel.__init__(self, **kwargs)

    @classmethod
    @abstractmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        cls._raise_not_implemented_error()

    @classmethod
    def rebuild_context_for_kwargs(
            cls,
            parent_kwargs: Kwargs,
            context: Optional["PromptContext"] = None
    ) -> "PromptContext":
        if not parent_kwargs:
            # Keep same context as we don't see a reason to recreate one.
            if context:
                return context
            else:
                return PromptContext.create_from_kwargs({})

        if context:
            kwargs = PromptContext.create_kwargs_from_context(
                context=context,
            )

            kwargs.update(parent_kwargs)
            parent_kwargs = kwargs

        return PromptContext.create_from_parent_context_and_kwargs(
            parent_context=context.parent_context if context else None,
            kwargs=parent_kwargs
        )

    def render(self, context: Optional["PromptContext"] = None) -> str:
        """Render the complete response."""
        rendered_lines = []

        # Creating a context allows to execute render without any extra information,
        # but manager parameters like terminal width are not available in this case.
        context = context or PromptContext.create_from_kwargs({})

        print(self.verbosity)
        print(context.verbosity)

        if self.verbosity <= context.verbosity:
            for line in self.lines:
                rendered = line.render(context)
                rendered_lines.append(rendered)

        return "\n".join(rendered_lines)
