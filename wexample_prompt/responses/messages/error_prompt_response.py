from typing import ClassVar, Optional, Type, TYPE_CHECKING

from wexample_prompt.responses.messages.abstract_message_response import AbstractMessageResponse

if TYPE_CHECKING:
    from wexample_prompt.example.abstract_response_example import AbstractResponseExample
    from wexample_prompt.enums.terminal_color import TerminalColor


class ErrorPromptResponse(AbstractMessageResponse):
    SYMBOL: ClassVar[str] = "❌"

    @classmethod
    def create_error(
            cls: "ErrorPromptResponse",
            message: Optional[str] = None,
            color: Optional["TerminalColor"] = None,
    ) -> "ErrorPromptResponse":
        from wexample_prompt.enums.terminal_color import TerminalColor

        return cls._create_symbol_message(
            text=message,
            color=color or TerminalColor.RED
        )

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        from wexample_prompt.example.response.messages.error_example import ErrorExample
        return ErrorExample
