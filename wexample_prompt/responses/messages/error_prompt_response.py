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

        # Build a simple text from message and/or exception.
        # Priority: explicit message > exception message > generic fallback.
        if message is not None and message != "":
            text = message
        elif exception is not None:
            # Keep it simple for now: just str(exception)
            # (later we can add type and traceback formatting)
            try:
                text = str(exception) if str(exception) else exception.__class__.__name__
            except Exception:
                text = exception.__class__.__name__
        else:
            text = "An error occurred"

        return cls._create_symbol_message(
            text=text,
            color=(color or TerminalColor.RED) if exception is None else TerminalColor.RESET,
            verbosity=verbosity
        )
