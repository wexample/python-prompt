from typing import TYPE_CHECKING, Optional

from wexample_helpers.const.types import Kwargs
from wexample_prompt.const.types import LineMessage

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.responses.messages.failure_prompt_response import FailurePromptResponse
    from wexample_prompt.common.io_manager import IoManager


class FailurePromptResponseManagerMixin:
    def failure(
            self: "IoManager",
            message: LineMessage,
            context: Optional["PromptContext"] = None,
            **kwargs: Kwargs
    ) -> "FailurePromptResponse":
        from wexample_prompt.responses.messages.failure_prompt_response import FailurePromptResponse

        response = FailurePromptResponse.create_failure(
            message=message,
        )

        return self.print_response(
            response=response,
            context=FailurePromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs
            )
        )
