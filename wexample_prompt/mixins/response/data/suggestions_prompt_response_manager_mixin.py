"""Mixin for handling suggestions responses in IoManager."""

from typing import TYPE_CHECKING

from wexample_helpers.const.types import Kwargs

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.const.types import LineMessage
from wexample_prompt.enums.verbosity_level import VerbosityLevel

if TYPE_CHECKING:
    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.responses.data.suggestions_prompt_response import (
        SuggestionsPromptResponse,
    )


class SuggestionsPromptResponseManagerMixin:
    """Mixin for IoManager to handle suggestions responses."""

    def suggestions(
        self: "IoManager",
        message: LineMessage,
        suggestions: list[str],
        arrow_style: str = "→",
        verbosity: VerbosityLevel | None = VerbosityLevel.DEFAULT,
        context: PromptContext | None = None,
        **kwargs: Kwargs,
    ) -> "SuggestionsPromptResponse":
        from wexample_prompt.responses.data.suggestions_prompt_response import (
            SuggestionsPromptResponse,
        )

        response = SuggestionsPromptResponse.create_suggestions(
            message=message,
            suggestions=suggestions,
            arrow_style=arrow_style,
            verbosity=verbosity,
        )

        return self.print_response(
            response=response,
            context=SuggestionsPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
        )
