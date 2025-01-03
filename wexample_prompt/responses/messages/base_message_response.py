from abc import abstractmethod
from typing import List, Optional, ClassVar

from pydantic import BaseModel

from wexample_prompt.common.color_manager import ColorManager
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.responses.base_prompt_response import BasePromptResponse


class BaseMessageResponse(BasePromptResponse, BaseModel):
    """Base class for all message responses."""
    
    # Symbol to display before the message, override in subclasses
    SYMBOL: ClassVar[str] = ""
    
    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True
    
    @classmethod
    @abstractmethod
    def get_message_type(cls) -> MessageType:
        """Get the message type for this response."""
        pass
    
    @classmethod
    def _create_symbol_message(
        cls,
        text: str,
        color: TerminalColor,
        symbol: Optional[str] = None,
        bold_symbol: bool = True
    ) -> 'BaseMessageResponse':
        """Create a message with an optional symbol.
        
        Args:
            text (str): The message text
            color (TerminalColor): The color to use
            symbol (Optional[str]): The symbol to use, defaults to cls.SYMBOL
            bold_symbol (bool): Whether to make the symbol bold
            
        Returns:
            BaseMessageResponse: A new message response
        """
        segments = []
        
        # Add symbol if present
        if symbol or cls.SYMBOL:
            symbol_text = f"{symbol or cls.SYMBOL} "
            symbol_segment = PromptResponseSegment(
                text=ColorManager.colorize(
                    symbol_text,
                    color,
                    TerminalColor.BOLD if bold_symbol else None
                )
            )
            segments.append(symbol_segment)
        
        # Add message text
        message = PromptResponseSegment(
            text=ColorManager.colorize(text, color)
        )
        segments.append(message)
        
        # Create line with segments
        line = PromptResponseLine(
            segments=segments,
            line_type=cls.get_message_type()
        )
        
        return cls(lines=[line], message_type=cls.get_message_type())
