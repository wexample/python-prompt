from wexample_prompt.common.color_manager import ColorManager
from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.enums.terminal_color import TerminalColor

class LogPromptResponse(BaseMessageResponse):
    """Response for log messages."""
    
    @classmethod
    def create(cls, text: str) -> 'LogPromptResponse':
        """Create a log message.
        
        Args:
            text (str): The log message text
            
        Returns:
            LogPromptResponse: A new log response
        """
        # Create the message segment with gray color
        message = PromptResponseSegment(
            text=ColorManager.colorize(text, TerminalColor.GRAY)
        )
        
        # Create a line with the message
        line = PromptResponseLine(
            segments=[message],
            line_type=cls.get_message_type()
        )
        
        return cls(lines=[line], message_type=cls.get_message_type())
    
    @classmethod
    def get_message_type(cls) -> MessageType:
        """Get the message type for log messages."""
        return MessageType.LOG
