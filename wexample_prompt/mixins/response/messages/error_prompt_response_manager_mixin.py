from typing import TYPE_CHECKING, Optional

from wexample_helpers.const.types import Kwargs

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.responses.messages.error_prompt_response import ErrorPromptResponse
    from wexample_prompt.common.io_manager import IoManager


class ErrorPromptResponseManagerMixin:
    def error(
            self: "IoManager",
            message: Optional[str] = None,
            exception: Optional[BaseException] = None,
            context: Optional["PromptContext"] = None,
            **kwargs: Kwargs
    ) -> "ErrorPromptResponse":
        from wexample_prompt.responses.messages.error_prompt_response import ErrorPromptResponse

        response = ErrorPromptResponse.create_error(
            message=message,
            exception=exception,
        )

        # Note: exception support is basic for now; detailed rendering (type/traceback)
        # will be added later.

        self.print_response(
            response=response,
            context=ErrorPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs
            )
        )

        return response
