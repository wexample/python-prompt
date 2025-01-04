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
        # Split text into lines
        text_lines = text.split('\n')
        lines = []
        
        # Create a line for each text line
        for text_line in text_lines:
            # Create the message segment with gray color
            message = PromptResponseSegment(
                text=ColorManager.colorize(text_line, TerminalColor.GRAY)
            )
            
            # Create a line with the message
            line = PromptResponseLine(
                segments=[message],
                line_type=cls.get_message_type()
            )
            lines.append(line)
        
        return cls(lines=lines, message_type=cls.get_message_type())
    
    @classmethod
    def get_message_type(cls) -> MessageType:
        """Get the message type for log messages."""
        return MessageType.LOG
