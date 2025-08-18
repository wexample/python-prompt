from typing import ClassVar, Type, TYPE_CHECKING, Optional

from wexample_prompt.responses.messages.abstract_message_response import AbstractMessageResponse

if TYPE_CHECKING:
    from wexample_prompt.example.abstract_response_example import AbstractResponseExample
    from wexample_prompt.enums.terminal_color import TerminalColor


class TaskPromptResponse(AbstractMessageResponse):
    SYMBOL: ClassVar[str] = "⚡"

    @classmethod
    def create_task(
        cls: "TaskPromptResponse",
        message: str,
        color: Optional["TerminalColor"] = None,
    ) -> "TaskPromptResponse":
        from wexample_prompt.enums.terminal_color import TerminalColor

        return cls._create_symbol_message(
            text=message,
            color=color or TerminalColor.YELLOW
        )

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        """Get the example class for task messages."""
        from wexample_prompt.example.response.messages.task_example import TaskExample
        return TaskExample
