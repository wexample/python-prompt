"""Interactive example for multiline_input - delegates to src example."""

from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class MultilineInputExample(AbstractPromptResponseExample):
    """Interactive example for multiline_input."""

    def execute(self) -> None:
        """Execute multiline input examples."""
        from wexample_prompt.example.response.interactive.multiline_input_example import (
            MultilineInputExample as SrcMultilineInputExample,
        )

        self.execute_delegated(SrcMultilineInputExample)
