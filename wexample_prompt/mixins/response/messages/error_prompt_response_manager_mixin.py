from typing import TYPE_CHECKING, Optional

from wexample_helpers.const.types import Kwargs

from wexample_prompt.enums.verbosity_level import VerbosityLevel

if TYPE_CHECKING:
    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.responses.messages.error_prompt_response import \
        ErrorPromptResponse


class ErrorPromptResponseManagerMixin:
    def error(
        self: "IoManager",
        message: Optional[str] = None,
        exception: Optional[BaseException] = None,
        verbosity: Optional[VerbosityLevel] = VerbosityLevel.DEFAULT,
        context: Optional["PromptContext"] = None,
        **kwargs: Kwargs
    ) -> "ErrorPromptResponse":
        from wexample_prompt.responses.messages.error_prompt_response import \
            ErrorPromptResponse

        response = ErrorPromptResponse.create_error(
            message=message,
            exception=exception,
            verbosity=verbosity,
        )

        return self.print_response(
            response=response,
            context=ErrorPromptResponse.rebuild_context_for_kwargs(
                context=context, parent_kwargs=kwargs
            ),
        )
