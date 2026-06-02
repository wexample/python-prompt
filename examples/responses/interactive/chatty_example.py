"""Interactive example for chatty - delegates to src example."""

from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class ChattyExample(AbstractPromptResponseExample):
    """Interactive example for chatty."""

    def execute(self) -> None:
        """Execute chatty example."""
        from wexample_prompt.example.response.interactive.chatty_example import (
            ChattyExample as SrcChattyExample,
        )

        self.execute_delegated(SrcChattyExample)
