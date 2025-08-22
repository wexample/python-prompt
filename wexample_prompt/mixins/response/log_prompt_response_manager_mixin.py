from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.const.types import Kwargs

from wexample_prompt.const.types import LineMessage
from wexample_prompt.enums.verbosity_level import VerbosityLevel

if TYPE_CHECKING:
    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.responses.abstract_prompt_response import (
        AbstractPromptResponse,
    )


class LogPromptResponseManagerMixin:
    def log(
        self: IoManager,
        message: LineMessage,
        verbosity: VerbosityLevel = VerbosityLevel.DEFAULT,
        context: PromptContext | None = None,
        **kwargs: Kwargs,
    ) -> AbstractPromptResponse:
        from wexample_prompt.responses.log_prompt_response import LogPromptResponse

        response = LogPromptResponse.create_log(
            message=message,
            verbosity=verbosity,
        )

        return self.print_response(
            response=response,
            context=LogPromptResponse.rebuild_context_for_kwargs(
                context=context, parent_kwargs=kwargs
            ),
        )
