from abc import ABC, abstractmethod

from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.enums.color import Color


class AbstractPromptTheme(ABC):
    """Base class for prompt themes."""
    
    @abstractmethod
    def get_color(self, message_type: MessageType) -> Color:
        """Get color for message type.
        
        Args:
            message_type: The type of message to get color for
            
        Returns:
            Color: Color for the message type
        """
        pass
