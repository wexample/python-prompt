from typing import ClassVar, Optional, Any, Type, TYPE_CHECKING

from wexample_prompt.common.error_context import ErrorContext
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses import BasePromptResponse
from wexample_prompt.responses.data.multiple_prompt_response import MultiplePromptResponse
from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse

if TYPE_CHECKING:
    from wexample_prompt.example.abstract_response_example import AbstractResponseExample


class ErrorPromptResponse(BaseMessageResponse):
    SYMBOL: ClassVar[str] = "❌"
    exception: Optional[Any] = None

    @classmethod
    def create_error(
        cls: "ErrorPromptResponse",
        message: Optional[str] = None,
        context: Optional[ErrorContext] = None,
        exception: Optional[Any] = None,
        color: Optional[TerminalColor] = None,
        **kwargs
    ) -> "ErrorPromptResponse":
        import traceback
        from wexample_prompt.enums.verbosity_level import VerbosityLevel

        # Build complete error message
        error_parts = []
        if message:
            error_parts.append(message)
        if exception:
            error_parts.append(str(exception))
            # Add traceback if there's an exception
            trace = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
            error_parts.append("\nTraceback:\n" + trace)

        # Create response with full error message
        response = cls._create_symbol_message(
            text="\n".join(error_parts) if error_parts else "Undefined error",
            color=color or TerminalColor.RED,
            context=context,
            **kwargs
        )

        response.exception = exception
        return response

    def is_fatal(self) -> bool:
        """Check if this is a fatal error."""
        if not isinstance(self.context, ErrorContext):
            return False
        return self.context.is_fatal

    def _on_fatal(self) -> None:
        """Handle fatal errors by raising the exception if present.

        Overrides BasePromptResponse._on_fatal()
        """
        # If we have an exception, raise it
        if self.context.fatal and self.exception:
            raise self.exception

    @classmethod
    def get_message_type(cls) -> MessageType:
        """Get the message type for error messages."""
        return MessageType.ERROR

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        """Get the example class for error messages."""
        from wexample_prompt.example.response.messages.error_example import ErrorExample
        return ErrorExample
