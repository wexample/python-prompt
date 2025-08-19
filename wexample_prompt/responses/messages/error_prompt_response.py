from typing import ClassVar, Optional, Type, TYPE_CHECKING

from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.responses.messages.abstract_message_response import AbstractMessageResponse

if TYPE_CHECKING:
    from wexample_prompt.example.abstract_response_example import AbstractResponseExample
    from wexample_prompt.enums.terminal_color import TerminalColor


class ErrorPromptResponse(AbstractMessageResponse):
    SYMBOL: ClassVar[str] = "❌"

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        from wexample_prompt.example.response.messages.error_example import ErrorExample
        return ErrorExample

    @classmethod
    def create_error(
            cls: "ErrorPromptResponse",
            message: Optional[str] = None,
            exception: Optional[BaseException] = None,
            color: Optional["TerminalColor"] = None,
            verbosity: VerbosityLevel = VerbosityLevel.DEFAULT
    ) -> "ErrorPromptResponse":
        from wexample_prompt.enums.terminal_color import TerminalColor

        # Build text using helpers when we have an exception; otherwise use the plain message or a fallback.
        if exception is not None:
            # Use existing debug/trace helpers to format the exception directly.
            # We keep the response color neutral so helper formatting (incl. ANSI) can pass through untouched.
            from wexample_helpers.helpers.error import error_format

            formatted = error_format(error=exception)
            if message is not None and message != "":
                text = f"{message}\n{formatted}"
            else:
                text = formatted
        else:
            text = message if (message is not None and message != "") else "An error occurred"

        return cls._create_symbol_message(
            text=text,
            color=(color or TerminalColor.RED) if exception is None else TerminalColor.RESET,
            verbosity=verbosity
        )
