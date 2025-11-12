"""Interactive example for tree - delegates to src example."""

from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class TreeExample(AbstractPromptResponseExample):
    """Interactive example for tree."""

    def execute(self) -> None:
        """Execute tree examples."""
        from wexample_prompt.example.response.data.tree_example import (
            TreeExample as SrcTreeExample,
        )

        self.execute_delegated(SrcTreeExample)
