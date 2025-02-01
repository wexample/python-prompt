from typing import ClassVar, TYPE_CHECKING, Optional

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse

if TYPE_CHECKING:
    from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse


class DebugPromptResponseIoManagerMixin:
    """Mixin for IoManager to handle debug responses."""

    def debug(self, message: str, **kwargs) -> "DebugPromptResponse":
        """Create and display a debug response."""
        response = DebugPromptResponse.create_debug(
            message=message,
            context=self._create_context(),
        )

        if self._logger.handlers:
            self._logger.debug(message)

        self.print_response(response)
        return response


class DebugPromptResponsePromptContextMixin:
    """Mixin for WithPromptContext to handle debug responses with context formatting."""

    def debug(self, message: str, **kwargs) -> "DebugPromptResponse":
        """Create and display a debug response with context formatting."""
        formatted_message = self.format_message(message)
        return self.io.debug(formatted_message, **kwargs)


class DebugPromptResponse(BaseMessageResponse):
    SYMBOL: ClassVar[str] = "🔍"

    @classmethod
    def create_debug(
        cls: "DebugPromptResponse",
        message: str,
        context: PromptContext = None,
        **kwargs
    ) -> "AbstractPromptResponse":
        return cls._create_symbol_message(
            text=message,
            context=context,
            color=TerminalColor.CYAN,
            **kwargs
        )

    @classmethod
    def get_message_type(cls) -> MessageType:
        """Get the message type for debug messages."""
        return MessageType.DEBUG
