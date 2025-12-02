"""Interactive example for list - delegates to src example."""
from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class ListExample(AbstractPromptResponseExample):
    """Interactive example for list."""

    def execute(self) -> None:
        """Execute list examples."""
        from wexample_prompt.example.response.data.list_example import (
            ListExample as SrcListExample,
        )

        self.execute_delegated(SrcListExample)
