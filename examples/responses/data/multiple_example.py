"""Interactive example for multiple - delegates to src example."""

from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class MultipleExample(AbstractPromptResponseExample):
    """Interactive example for multiple."""

    def execute(self) -> None:
        """Execute multiple examples."""
        from wexample_prompt.example.response.data.multiple_example import (
            MultipleExample as SrcMultipleExample,
        )

        self.execute_delegated(SrcMultipleExample)
