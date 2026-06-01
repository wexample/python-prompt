from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from wexample_helpers.const.types import Kwargs

    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.const.types import LineMessage
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.responses.interactive.multiline_input_prompt_response import (
        MultilineInputPromptResponse,
    )


class MultilineInputPromptResponseManagerMixin:
    def multiline_input(
        self: IoManager,
        question: LineMessage | None = "Type your message (Esc+Enter for newline, Enter to submit):",
        default_value: str | None = None,
        predefined_answer: Any = None,
        prompt_prefix: str = "❯ ",
        bordered: bool = False,
        footer_hint: str | None = None,
        reset_on_finish: bool = False,
        verbosity: VerbosityLevel | None = None,
        context: PromptContext | None = None,
        **kwargs: Kwargs,
    ) -> MultilineInputPromptResponse:
        from wexample_prompt.responses.interactive.multiline_input_prompt_response import (
            MultilineInputPromptResponse,
        )

        response = MultilineInputPromptResponse.create_multiline_input(
            question=question,
            default_value=default_value,
            predefined_answer=predefined_answer,
            prompt_prefix=prompt_prefix,
            bordered=bordered,
            footer_hint=footer_hint,
            reset_on_finish=reset_on_finish,
        )

        return self.print_response(
            response=response,
            context=MultilineInputPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
        )
