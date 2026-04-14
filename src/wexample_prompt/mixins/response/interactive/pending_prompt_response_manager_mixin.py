from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_prompt.enums.terminal_color import TerminalColor

if TYPE_CHECKING:
    from collections.abc import Callable

    from wexample_helpers.const.types import Kwargs

    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.responses.interactive.pending_prompt_response import (
        PendingPromptResponse,
    )


class PendingPromptResponseManagerMixin:
    def pending(
        self: IoManager,
        *,
        callback: Callable[[], tuple[bool, list[str]]],
        label: str = "Waiting...",
        interval: float = 2.0,
        max_lines: int = 5,
        output_color: TerminalColor | None = TerminalColor.LIGHT_BLACK,
        reset_on_finish: bool = False,
        verbosity: VerbosityLevel | None = None,
        context: PromptContext | None = None,
        **kwargs: Kwargs,
    ) -> PendingPromptResponse:
        from wexample_prompt.responses.interactive.pending_prompt_response import (
            PendingPromptResponse,
        )

        response = PendingPromptResponse.create_pending(
            callback=callback,
            label=label,
            interval=interval,
            max_lines=max_lines,
            output_color=output_color,
            reset_on_finish=reset_on_finish,
        )

        return self.print_response(
            response=response,
            context=PendingPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
        )
