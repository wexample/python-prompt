from enum import Enum
from wexample_prompt.enums.message_type import MessageType


class MessageColor:
    """ANSI color codes for different message types."""
    
    # Color codes
    _COLORS = {
        MessageType.ALERT: "\033[93m",      # Bright yellow
        MessageType.CRITICAL: "\033[91m",   # Bright red
        MessageType.DEBUG: "\033[36m",      # Cyan
        MessageType.ERROR: "\033[31m",      # Red
        MessageType.FAILURE: "\033[31m",    # Red
        MessageType.INFO: "\033[94m",       # Bright blue
        MessageType.LOG: "",                # Default color
        MessageType.SUCCESS: "\033[32m",    # Green
        MessageType.TASK: "\033[95m",       # Magenta
        MessageType.WARNING: "\033[33m",    # Yellow
    }
    
    @classmethod
    def get_color_code(cls, message_type: MessageType) -> str:
        """Get the ANSI color code for a message type."""
        return cls._COLORS.get(message_type, "")
