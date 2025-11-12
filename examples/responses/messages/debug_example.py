"""Interactive example for debug - delegates to src example."""

from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class DebugExample(AbstractPromptResponseExample):
    """Interactive example for debug."""

    def execute(self) -> None:
        """Execute debug examples."""
        from wexample_prompt.example.response.messages.debug_example import (
            DebugExample as SrcDebugExample,
        )

        self.execute_delegated(SrcDebugExample)
