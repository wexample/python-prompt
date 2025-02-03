from typing import TYPE_CHECKING, Optional, Any

from wexample_prompt.common.error_context import ErrorContext

if TYPE_CHECKING:
    from wexample_prompt.responses.messages import ErrorPromptResponse


class ErrorPromptResponseManagerMixin:
    def error(
        self,
        message: str,
        exception: Optional[Any] = None,
        fatal: bool = False,
        **kwargs
    ) -> "ErrorPromptResponse":
        from wexample_prompt.responses.messages import ErrorPromptResponse

        base_context = self.create_context()
        context = ErrorContext(**base_context.model_dump(), is_fatal=fatal)

        response = ErrorPromptResponse.create_error(
            message=message,
            context=context,
            exception=exception,
            **kwargs
        )

        self.print_response(response)
        response._on_fatal()
        return response
