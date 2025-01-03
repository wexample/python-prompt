from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse
from wexample_prompt.enums.message_type import MessageType


class FailurePromptResponse(BaseMessageResponse):
    """Response for failure messages."""
    
    @classmethod
    def get_message_type(cls) -> MessageType:
        return MessageType.FAILURE
