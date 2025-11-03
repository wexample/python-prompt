"""Interactive example for success - delegates to src example."""

from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class SuccessExample(AbstractPromptResponseExample):
    """Interactive example for success."""

    def execute(self) -> None:
        """Execute success examples."""
        from wexample_prompt.example.response.messages.success_example import (
            SuccessExample as SrcSuccessExample,
        )

        self.execute_delegated(SrcSuccessExample)
