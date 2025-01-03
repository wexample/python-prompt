from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse
from wexample_prompt.enums.message_type import MessageType


class DebugPromptResponse(BaseMessageResponse):
    """Response for debug messages."""
    
    @classmethod
    def get_message_type(cls) -> MessageType:
        return MessageType.DEBUG
