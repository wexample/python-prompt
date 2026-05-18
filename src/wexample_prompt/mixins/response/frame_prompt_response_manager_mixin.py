from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_helpers.const.types import Kwargs

    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.enums.terminal_color import TerminalColor
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.responses.abstract_prompt_response import (
        AbstractPromptResponse,
    )
    from wexample_prompt.responses.frame_prompt_response import FramePromptResponse


class FramePromptResponseManagerMixin:
    def frame(
        self: IoManager,
        text: str | list[str] | None = None,
        responses: list[AbstractPromptResponse] | None = None,
        title: str | None = None,
        border_color: TerminalColor | None = None,
        padding: int = 1,
        verbosity: VerbosityLevel | None = None,
        context: PromptContext | None = None,
        **kwargs: Kwargs,
    ) -> FramePromptResponse:
        from wexample_prompt.responses.frame_prompt_response import FramePromptResponse

        response = FramePromptResponse.create_frame(
            text=text,
            responses=responses,
            title=title,
            border_color=border_color,
            padding=padding,
            verbosity=(
                verbosity if verbosity is not None else self.default_response_verbosity
            ),
        )

        return self.print_response(
            response=response,
            context=FramePromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
        )
