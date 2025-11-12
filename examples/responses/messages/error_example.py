"""Interactive example for error messages - delegates to src example."""

from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class ErrorExample(AbstractPromptResponseExample):
    """Interactive example for error messages with edge cases."""

    def execute(self) -> None:
        """Execute comprehensive error examples including edge cases."""
        from wexample_prompt.example.response.messages.error_example import (
            ErrorExample as SrcErrorExample,
        )

        self.execute_delegated(SrcErrorExample)
