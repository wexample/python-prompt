from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse
from wexample_prompt.enums.message_type import MessageType


class TaskPromptResponse(BaseMessageResponse):
    """Response for task messages."""
    
    @classmethod
    def get_message_type(cls) -> MessageType:
        return MessageType.TASK
