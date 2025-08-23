from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from wexample_prompt.const.types import LineMessage
from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.responses.messages.abstract_message_response import (
    AbstractMessageResponse,
)

if TYPE_CHECKING:
    from wexample_prompt.enums.terminal_color import TerminalColor
    from wexample_prompt.example.abstract_response_example import (
        AbstractResponseExample,
    )


class FailurePromptResponse(AbstractMessageResponse):
    """Response for failure messages."""

    SYMBOL: ClassVar[str] = "❌"

    @classmethod
    def create_failure(
        cls: FailurePromptResponse,
        message: LineMessage,
        color: TerminalColor | None = None,
        verbosity: VerbosityLevel = VerbosityLevel.DEFAULT,
    ) -> FailurePromptResponse:
        from wexample_prompt.enums.terminal_color import TerminalColor

        return cls._create_symbol_message(
            text=message, color=color or TerminalColor.RED, verbosity=verbosity
        )

    @classmethod
    def get_example_class(cls) -> type[AbstractResponseExample]:
        from wexample_prompt.example.response.messages.failure_example import (
            FailureExample,
        )

        return FailureExample
