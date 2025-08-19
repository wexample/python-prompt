from typing import TYPE_CHECKING, Optional, Any

from wexample_helpers.const.types import Kwargs

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.common.io_manager import IoManager


class SuccessPromptResponseManagerMixin:
    def success(
            self: "IoManager",
            message: str,
            context: Optional["PromptContext"] = None,
            **kwargs: Kwargs
    ) -> Any:
        from wexample_prompt.responses.messages.success_prompt_response import SuccessPromptResponse

        response = SuccessPromptResponse.create_success(
            message=message,
        )

        return self.print_response(
            response=response,
            context=SuccessPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs
            )
        )
