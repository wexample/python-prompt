from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse
from wexample_prompt.enums.message_type import MessageType


class ErrorPromptResponse(BaseMessageResponse):
    """Response for error messages."""
    
    @classmethod
    def get_message_type(cls) -> MessageType:
        return MessageType.ERROR
