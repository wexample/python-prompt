from typing import ClassVar, Type, TYPE_CHECKING, Optional

from wexample_prompt.responses.messages.abstract_message_response import AbstractMessageResponse

if TYPE_CHECKING:
    from wexample_prompt.example.abstract_response_example import AbstractResponseExample
    from wexample_prompt.enums.terminal_color import TerminalColor


class FailurePromptResponse(AbstractMessageResponse):
    """Response for failure messages."""

    SYMBOL: ClassVar[str] = "❌"

    @classmethod
    def create_failure(
            cls: "FailurePromptResponse",
            message: str,
            color: Optional["TerminalColor"] = None,
    ) -> "FailurePromptResponse":
        from wexample_prompt.enums.terminal_color import TerminalColor

        return cls._create_symbol_message(
            text=message,
            color=color or TerminalColor.RED,
        )

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        from wexample_prompt.example.response.messages.failure_example import FailureExample
        return FailureExample
