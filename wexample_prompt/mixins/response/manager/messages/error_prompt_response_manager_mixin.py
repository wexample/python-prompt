from typing import TYPE_CHECKING, Optional, Any, Dict

from wexample_prompt.common.error_context import ErrorContext

if TYPE_CHECKING:
    from wexample_prompt.responses.messages import ErrorPromptResponse


class ErrorPromptResponseManagerMixin:
    def error(
        self,
        message: str,
        params: Optional[Dict[str, Any]] = None,
        exception: Optional[Any] = None,
        fatal: bool = False,
        **kwargs
    ) -> "ErrorPromptResponse":
        from wexample_prompt.responses.messages import ErrorPromptResponse

        context = ErrorContext(
            fatal=fatal,
            params=params,
            indentation=self.log_indent
        )
        response = ErrorPromptResponse.create_error(
            message=message,
            context=context,
            exception=exception,
            **kwargs
        )

        # Log to file/system if configured
        if self._logger.handlers:
            self._logger.error(message, extra={"params": params} if params else None)

        self.print_response(response)
        response._on_fatal()
        return response
