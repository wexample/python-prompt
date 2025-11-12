"""Interactive example for failure - delegates to src example."""

from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class FailureExample(AbstractPromptResponseExample):
    """Interactive example for failure."""

    def execute(self) -> None:
        """Execute failure examples."""
        from wexample_prompt.example.response.messages.failure_example import (
            FailureExample as SrcFailureExample,
        )

        self.execute_delegated(SrcFailureExample)
