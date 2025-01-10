from typing import ClassVar, Optional
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.messages.base_message_response import BaseMessageResponse
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.common.prompt_context import PromptContext


class DebugPromptResponse(BaseMessageResponse):
    """Response for debug messages."""
    
    SYMBOL: ClassVar[str] = "🔍"
    
    @classmethod
    def create(cls, text: str, context: Optional[PromptContext] = None) -> 'DebugPromptResponse':
        """Create a debug message.
        
        Args:
            text (str): The debug message text
            context: Optional context for this response
            
        Returns:
            DebugPromptResponse: A new debug response
        """
        return cls._create_symbol_message(text, TerminalColor.CYAN, context=context)
    
    @classmethod
    def get_message_type(cls) -> MessageType:
        """Get the message type for debug messages."""
        return MessageType.DEBUG
