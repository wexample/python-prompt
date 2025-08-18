from typing import TYPE_CHECKING, Optional

from wexample_helpers.const.types import Kwargs

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.responses.messages import FailurePromptResponse


class FailurePromptResponseManagerMixin:
    def failure(
            self,
            message: str,
            context: Optional["PromptContext"] = None,
            **kwargs: Kwargs
    ) -> "FailurePromptResponse":
        from wexample_prompt.responses.messages.failure_prompt_response import FailurePromptResponse

        response = FailurePromptResponse.create_failure(
            message=message,
        )

        self.print_response(
            response=response,
            context=FailurePromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs
            )
        )

        return response
