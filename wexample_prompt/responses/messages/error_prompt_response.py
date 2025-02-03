from typing import ClassVar, Optional, Any, Type, TYPE_CHECKING
import traceback

from wexample_prompt.common.error_context import ErrorContext
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse
from wexample_prompt.responses.base_prompt_response import BasePromptResponse
from wexample_prompt.responses.data.multiple_prompt_response import MultiplePromptResponse
from wexample_prompt.enums.verbosity_level import VerbosityLevel

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

        if exception is not None:
            message += f': {exception}'

        # Create response with context
        response = cls._create_symbol_message(
            text=message or "Undefined error",
            color=color or TerminalColor.RED,
            context=context,
            **kwargs
        )

        response.exception = exception

        # Add exception details if present
        if exception is not None:
            # Get full traceback
            trace = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
            
            # Create detailed response with trace
            response_details = BasePromptResponse.create_from_text(
                text=trace,
                context=context,
                verbosity_level=VerbosityLevel.DEFAULT
            )
            
            # Combine responses
            response = MultiplePromptResponse.create_multiple(
                responses=[
                    response,
                    response_details,
                ],
                context=context
            )

        return response

    def is_fatal(self) -> bool:
        """Check if this is a fatal error."""
        if not isinstance(self.context, ErrorContext):
            return False
        return self.context.is_fatal

    def _on_fatal(self):
        """Handle fatal errors by raising the exception if present."""
        if self.is_fatal() and self.exception:
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
