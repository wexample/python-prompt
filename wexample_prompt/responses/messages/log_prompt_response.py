"""Response for log messages."""
from typing import Type, TYPE_CHECKING

from wexample_prompt.common.color_manager import ColorManager
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse

if TYPE_CHECKING:
    from wexample_prompt.enums.message_type import MessageType
    from wexample_prompt.example.abstract_response_example import AbstractResponseExample


class LogPromptResponse(BaseMessageResponse):
    """Response for log messages."""

    @classmethod
    def create_log(
        cls,
        message: str,
        context: PromptContext = None,
        **kwargs
    ) -> "LogPromptResponse":
        """Create a log message."""
        lines = []
        segments = []

        # Add message text
        message_segment = PromptResponseSegment(
            text=ColorManager.colorize(message, TerminalColor.WHITE)
        )
        segments.append(message_segment)

        # Create line with segments
        line = PromptResponseLine(
            segments=segments,
            line_type=cls.get_message_type()
        )
        lines.append(line)

        return cls(
            lines=lines,
            context=context,
            message_type=cls.get_message_type(),
            **kwargs)

    @classmethod
    def get_message_type(cls) -> "MessageType":
        from wexample_prompt.enums.message_type import MessageType

        return MessageType.LOG

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        """Get the example class for log messages."""
        from wexample_prompt.example.response.messages.log_example import LogExample
        return LogExample
