from typing import TYPE_CHECKING, ClassVar, Optional, Type

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


class TaskPromptResponse(AbstractMessageResponse):
    SYMBOL: ClassVar[str] = "⚡"

    @classmethod
    def create_task(
        cls: "TaskPromptResponse",
        message: LineMessage,
        color: Optional["TerminalColor"] = None,
        verbosity: VerbosityLevel = VerbosityLevel.DEFAULT,
    ) -> "TaskPromptResponse":
        from wexample_prompt.enums.terminal_color import TerminalColor

        return cls._create_symbol_message(
            text=message, color=color or TerminalColor.YELLOW, verbosity=verbosity
        )

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        """Get the example class for task messages."""
        from wexample_prompt.example.response.messages.task_example import TaskExample

        return TaskExample
