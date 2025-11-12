"""Interactive example for progress bars - delegates to src example."""

from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class ProgressExample(AbstractPromptResponseExample):
    """Interactive example for progress bars with edge cases."""

    def execute(self) -> None:
        """Execute comprehensive progress examples including edge cases."""
        from wexample_prompt.example.response.interactive.progress_example import (
            ProgressExample as SrcProgressExample,
        )

        self.execute_delegated(SrcProgressExample)
