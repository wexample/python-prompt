from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse
from wexample_prompt.enums.message_type import MessageType


class CriticalPromptResponse(BaseMessageResponse):
    """Response for critical messages."""
    
    @classmethod
    def get_message_type(cls) -> MessageType:
        return MessageType.CRITICAL
