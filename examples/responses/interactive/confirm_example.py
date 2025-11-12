"""Interactive example for confirm prompts - delegates to src example."""

from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class ConfirmExample(AbstractPromptResponseExample):
    """Interactive example for confirm prompts with edge cases."""

    def execute(self) -> None:
        """Execute comprehensive confirm examples including edge cases."""
        from wexample_prompt.example.response.interactive.confirm_example import (
            ConfirmExample as SrcConfirmExample,
        )

        self.execute_delegated(SrcConfirmExample)
