from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from wexample_helpers.const.types import Kwargs
from wexample_prompt.const.types import LineMessage
from wexample_prompt.enums.verbosity_level import VerbosityLevel

if TYPE_CHECKING:
    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.responses.messages.warning_prompt_response import (
        WarningPromptResponse,
    )


class WarningPromptResponseManagerMixin:
    def warning(
        self: "IoManager",
        message: LineMessage,
        verbosity: VerbosityLevel | None = VerbosityLevel.DEFAULT,
        context: Optional["PromptContext"] = None,
        **kwargs: Kwargs
    ) -> "WarningPromptResponse":
        from wexample_prompt.responses.messages.warning_prompt_response import (
            WarningPromptResponse,
        )

        response = WarningPromptResponse.create_warning(
            message=message,
            verbosity=verbosity,
        )

        return self.print_response(
            response=response,
            context=WarningPromptResponse.rebuild_context_for_kwargs(
                context=context, parent_kwargs=kwargs
            ),
        )
