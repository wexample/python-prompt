from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_helpers.const.types import Kwargs

    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.responses.interactive.spinner_prompt_response import (
        SpinnerPromptResponse,
    )


class SpinnerPromptResponseManagerMixin:
    def spinner(
        self: IoManager,
        label: str = "Thinking…",
        interval: float = 0.1,
        verbosity: VerbosityLevel | None = None,
        context: PromptContext | None = None,
        **kwargs: Kwargs,
    ) -> SpinnerPromptResponse:
        from wexample_prompt.responses.interactive.spinner_prompt_response import (
            SpinnerPromptResponse,
        )

        response = SpinnerPromptResponse.create_spinner(
            label=label, interval=interval
        )
        response.verbosity = (
            verbosity if verbosity is not None else self.default_response_verbosity
        )

        return self.print_response(
            response=response,
            context=SpinnerPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
        )
