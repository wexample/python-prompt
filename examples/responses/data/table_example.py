"""Interactive example for table - delegates to src example."""

from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class TableExample(AbstractPromptResponseExample):
    """Interactive example for table."""

    def execute(self) -> None:
        """Execute table examples."""
        from wexample_prompt.example.response.data.table_example import (
            TableExample as SrcTableExample,
        )

        self.execute_delegated(SrcTableExample)
