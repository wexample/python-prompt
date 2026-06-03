"""Interactive example for spinner - delegates to src example."""

from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class SpinnerExample(AbstractPromptResponseExample):
    """Interactive example for spinner."""

    def execute(self) -> None:
        """Execute spinner examples."""
        from wexample_prompt.example.response.interactive.spinner_example import (
            SpinnerExample as SrcSpinnerExample,
        )

        self.execute_delegated(SrcSpinnerExample)
