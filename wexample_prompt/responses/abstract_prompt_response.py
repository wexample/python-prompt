from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Optional

from pydantic import Field
from wexample_helpers.classes.extended_base_model import ExtendedBaseModel
from wexample_helpers.classes.mixin.has_snake_short_class_name_class_mixin import (
    HasSnakeShortClassNameClassMixin,
)
from wexample_helpers.const.types import Kwargs
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.enums.verbosity_level import VerbosityLevel

if TYPE_CHECKING:
    from wexample_prompt.example.abstract_response_example import (
        AbstractResponseExample,
    )


class AbstractPromptResponse(HasSnakeShortClassNameClassMixin, ExtendedBaseModel):
    """Abstract base class for all prompt responses."""

    lines: list[PromptResponseLine] = Field(
        default_factory=list,
        description="The list of lines of the response content",
    )
    verbosity: VerbosityLevel | None = Field(
        default=VerbosityLevel.DEFAULT,
        description="The context verbosity, saying which response to render or not",
    )
    _rendered_content: str | None = None

    @property
    def rendered_content(self) -> str | None:
        return self._rendered_content

    @classmethod
    def get_class_name_suffix(cls) -> str | None:
        return "PromptResponse"

    @classmethod
    def _create(
        cls: AbstractPromptResponse,
        lines: list[PromptResponseLine],
        **kwargs,
    ) -> AbstractPromptResponse:
        """Create a new response with the given lines."""
        return cls(lines=lines, **kwargs)

    @classmethod
    @abstractmethod
    def get_example_class(cls) -> type["AbstractResponseExample"]:
        cls._raise_not_implemented_error()

    @classmethod
    def rebuild_context_for_kwargs(
        cls,
        parent_kwargs: Kwargs,
        context: Optional["PromptContext"] = None,
    ) -> PromptContext:
        if not parent_kwargs:
            # Keep same context as we don't see a reason to recreate one.
            return context or PromptContext.create_from_kwargs({})

        if context:
            kwargs = PromptContext.create_kwargs_from_context(context=context)
            kwargs.update(parent_kwargs)
            parent_kwargs = kwargs

        return PromptContext.create_from_parent_context_and_kwargs(
            parent_context=context.parent_context if context else None,
            kwargs=parent_kwargs,
        )

    def reset(self) -> None:
        self._rendered_content = None

    def render(self, context: Optional["PromptContext"] = None) -> str | None:
        """Render the complete response."""

        context = PromptContext.create_if_none(context=context)

        if self.verbosity > context.verbosity:
            return None

        self._rendered_content = "\n".join(line.render(context) for line in self.lines)
        return self._rendered_content
