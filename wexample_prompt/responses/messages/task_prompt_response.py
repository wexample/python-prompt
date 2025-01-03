from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse
from wexample_prompt.enums.message_type import MessageType


class TaskPromptResponse(BaseMessageResponse):
    """Response for task messages."""

    @classmethod
    def create(cls, text: str) -> 'TaskPromptResponse':
        """Create a warning message.

        Args:
            text (str): The warning message text

        Returns:
            WarningPromptResponse: A new warning response
        """
        return cls._create_symbol_message(text, TerminalColor.YELLOW)
    
    @classmethod
    def get_message_type(cls) -> MessageType:
        return MessageType.TASK
