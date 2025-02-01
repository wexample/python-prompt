from typing import ClassVar, TYPE_CHECKING

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse

if TYPE_CHECKING:
    from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse


class InfoPromptResponseIoManagerMixin:
    """Mixin for IoManager to handle info responses."""

    def info(self, message: str, **kwargs) -> "InfoPromptResponse":
        """Create and display an info response."""
        response = InfoPromptResponse.create_info(
            message=message,
            context=self._create_context(),
        )

        if self._logger.handlers:
            self._logger.info(message)

        self.print_response(response)
        return response


class InfoPromptResponsePromptContextMixin:
    """Mixin for WithPromptContext to handle info responses with context formatting."""

    def info(self, message: str, **kwargs) -> "InfoPromptResponse":
        """Create and display an info response with context formatting."""
        formatted_message = self.format_message(message)
        return self.io.info(formatted_message, **kwargs)


class InfoPromptResponse(BaseMessageResponse):
    """Response for info messages."""
    SYMBOL: ClassVar[str] = "ℹ️"

    @classmethod
    def create_info(
        cls: "InfoPromptResponse",
        message: str,
        context: PromptContext = None,
        **kwargs
    ) -> "AbstractPromptResponse":
        return cls._create_symbol_message(
            text=message,
            context=context,
            color=TerminalColor.LIGHT_BLUE,
            **kwargs
        )

    @classmethod
    def get_message_type(cls) -> MessageType:
        """Get the message type for info messages."""
        return MessageType.INFO
