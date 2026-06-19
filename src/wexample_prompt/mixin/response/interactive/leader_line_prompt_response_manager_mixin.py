"""Mixin: `io.leader_line(...)` factory bound to the IoManager."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_helpers.const.types import Kwargs

    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.common.leader.leader_markers import LeaderLineMarkers
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.enums.terminal_color import TerminalColor
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.responses.interactive.leader_line_prompt_response import (
        LeaderLinePromptResponse,
    )


class LeaderLinePromptResponseManagerMixin:
    def leader_line(
        self: IoManager,
        message: str,
        state: str = "pending",
        status: str | None = None,
        markers: LeaderLineMarkers | None = None,
        dot_char: str = ".",
        dot_color: TerminalColor | None = None,
        width: int | None = None,
        verbosity: VerbosityLevel | None = None,
        context: PromptContext | None = None,
        print_response: bool = True,
        **kwargs: Kwargs,
    ) -> LeaderLinePromptResponse:
        from wexample_prompt.enums.terminal_color import TerminalColor
        from wexample_prompt.responses.interactive.leader_line_prompt_response import (
            LeaderLinePromptResponse,
        )

        response = LeaderLinePromptResponse.create_leader_line(
            message=message,
            state=state,
            status=status,
            markers=markers,
            dot_char=dot_char,
            dot_color=(
                dot_color if dot_color is not None else TerminalColor.LIGHT_BLACK
            ),
            width=width,
            verbosity=(
                verbosity if verbosity is not None else self.default_response_verbosity
            ),
        )

        rebuilt_context = LeaderLinePromptResponse.rebuild_context_for_kwargs(
            context=context,
            parent_kwargs=kwargs,
        )
        effective_context = self.create_context(context=rebuilt_context)

        # Always init the handle BEFORE printing — `print_response` may be
        # short-circuited by a QUIET verbosity (no render → no handle), and
        # callers still need a usable handle to bind to.
        response.init_handle(context=effective_context)

        if print_response:
            response = self.print_response(response=response, context=rebuilt_context)

        # Bind the IoManager's output so the handle can re-render in place.
        response.get_handle().output = self.output
        return response
