"""Mixin for managing free-text input prompts."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.const.types import LineMessage
    from wexample_prompt.responses.interactive.input_prompt_response import (
        InputPromptResponse,
    )


class InputPromptResponseManagerMixin:
    """Mixin class for managing free-text input prompt responses."""

    def input(
        self: IoManager,
        question: LineMessage = "Enter a value:",
        default_value: str | None = None,
        reset_on_finish: bool = False,
        context: PromptContext | None = None,
        predefined_answer: Any = None,
        **kwargs: Any,
    ) -> InputPromptResponse:
        from wexample_prompt.responses.interactive.input_prompt_response import (
            InputPromptResponse,
        )

        response = InputPromptResponse.create_input(
            question=question,
            default_value=default_value,
            predefined_answer=predefined_answer,
            reset_on_finish=reset_on_finish,
        )

        return self.print_response(
            response=response,
            context=InputPromptResponse.rebuild_context_for_kwargs(
                context=context, parent_kwargs=kwargs
            ),
        )
