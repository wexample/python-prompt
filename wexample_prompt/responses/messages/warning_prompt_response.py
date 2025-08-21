from typing import ClassVar, Type, TYPE_CHECKING, Optional

from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.responses.messages.abstract_message_response import (
    AbstractMessageResponse,
)
from wexample_prompt.const.types import LineMessage

if TYPE_CHECKING:
    from wexample_prompt.example.abstract_response_example import (
        AbstractResponseExample,
    )
    from wexample_prompt.enums.terminal_color import TerminalColor


class WarningPromptResponse(AbstractMessageResponse):
    """Response for warning messages."""

    SYMBOL: ClassVar[str] = "⚠"

    @classmethod
    def create_warning(
        cls: "WarningPromptResponse",
        message: LineMessage,
        color: Optional["TerminalColor"] = None,
        verbosity: VerbosityLevel = VerbosityLevel.DEFAULT,
    ) -> "WarningPromptResponse":
        from wexample_prompt.enums.terminal_color import TerminalColor

        return cls._create_symbol_message(
            text=message, color=color or TerminalColor.YELLOW, verbosity=verbosity
        )

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        """Get the example class for warning messages."""
        from wexample_prompt.example.response.messages.warning_example import (
            WarningExample,
        )

        return WarningExample
