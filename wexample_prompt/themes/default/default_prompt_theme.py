from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.themes.default.abstract_prompt_theme import AbstractPromptTheme
from wexample_prompt.core.colors import ColorManager, TerminalColor


class DefaultPromptTheme(AbstractPromptTheme):
    """Default theme for prompt responses."""
    
    def get_color(self, message_type: MessageType) -> TerminalColor:
        """Get color for message type."""
        return ColorManager.get_message_color(message_type)
