from typing import ClassVar, TYPE_CHECKING, Optional

from wexample_prompt.common.color_manager import ColorManager
from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.enums.terminal_color import TerminalColor

if TYPE_CHECKING:
    from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse


class LogPromptResponseIoManagerMixin:
    """Mixin for IoManager to handle log responses."""

    def log(self, message: str, **kwargs) -> "LogPromptResponse":
        """Create and display a log response."""
        response = LogPromptResponse.create_log(
            message=message,
            context=self._create_context(),
        )

        if self._logger.handlers:
            self._logger.debug(message)

        self.print_response(response)
        return response


class LogPromptResponsePromptContextMixin:
    """Mixin for WithPromptContext to handle log responses with context formatting."""

    def log(self, message: str, **kwargs) -> "LogPromptResponse":
        """Create and display a log response with context formatting."""
        formatted_message = self.format_message(message)
        return self.io.log(formatted_message, **kwargs)


class LogPromptResponse(BaseMessageResponse):
    """Response for log messages."""

    @classmethod
    def create_log(
        cls: "LogPromptResponse",
        message: str,
        context: PromptContext = None,
        **kwargs
    ) -> "AbstractPromptResponse":
        text_lines = message.split('\n')
        lines = []
        
        for text_line in text_lines:
            message_segment = PromptResponseSegment(
                text=ColorManager.colorize(text_line, TerminalColor.WHITE)
            )
            
            line = PromptResponseLine(
                segments=[message_segment],
                line_type=cls.get_message_type()
            )
            lines.append(line)
        
        return cls(lines=lines, context=context, message_type=cls.get_message_type())
    
    @classmethod
    def get_message_type(cls) -> MessageType:
        """Get the message type for log messages."""
        return MessageType.LOG
