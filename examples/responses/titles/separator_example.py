"""Interactive example for separator - delegates to src example."""

from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class SeparatorExample(AbstractPromptResponseExample):
    """Interactive example for separator."""

    def execute(self) -> None:
        """Execute separator examples."""
        from wexample_prompt.example.response.titles.separator_example import (
            SeparatorExample as SrcSeparatorExample,
        )

        self.execute_delegated(SrcSeparatorExample)
