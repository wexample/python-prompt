from typing import TYPE_CHECKING, Optional

from wexample_helpers.const.types import Kwargs

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.responses.messages.warning_prompt_response import WarningPromptResponse
    from wexample_prompt.common.io_manager import IoManager


class WarningPromptResponseManagerMixin:
    def warning(
            self: "IoManager",
            message: str,
            context: Optional["PromptContext"] = None,
            **kwargs: Kwargs
    ) -> "WarningPromptResponse":
        from wexample_prompt.responses.messages.warning_prompt_response import WarningPromptResponse

        response = WarningPromptResponse.create_warning(
            message=message,
        )

        self.print_response(
            response=response,
            context=WarningPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs
            )
        )

        return response
