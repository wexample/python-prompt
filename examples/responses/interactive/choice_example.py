"""Interactive example for choice prompts - delegates to src example."""

from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class ChoiceExample(AbstractPromptResponseExample):
    """Interactive example for choice prompts with edge cases."""

    def execute(self) -> None:
        """Execute comprehensive choice examples including edge cases."""
        from wexample_prompt.example.response.interactive.choice_example import (
            ChoiceExample as SrcChoiceExample,
        )

        self.execute_delegated(SrcChoiceExample)
