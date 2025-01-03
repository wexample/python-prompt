from wexample_prompt.enums.color import Color
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.themes.default.abstract_prompt_theme import AbstractPromptTheme


class DefaultPromptTheme(AbstractPromptTheme):
    """Default theme for prompt responses."""
    
    def get_color(self, message_type: MessageType) -> "Color":
        """Get color for message type."""
        return {
            MessageType.ERROR: Color.RED,
            MessageType.WARNING: Color.YELLOW,
            MessageType.SUCCESS: Color.GREEN,
            MessageType.INFO: Color.BLUE,
            MessageType.DEBUG: Color.GRAY,
            MessageType.CRITICAL: Color.LIGHT_RED,
            MessageType.ALERT: Color.MAGENTA,
            MessageType.TASK: Color.CYAN,
            MessageType.LOG: Color.GRAY,
            MessageType.FAILURE: Color.RED,
        }.get(message_type, Color.DEFAULT)
