"""Interactive example for warning - delegates to src example."""

from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class WarningExample(AbstractPromptResponseExample):
    """Interactive example for warning."""

    def execute(self) -> None:
        """Execute warning examples."""
        from wexample_prompt.example.response.messages.warning_example import (
            WarningExample as SrcWarningExample,
        )

        self.execute_delegated(SrcWarningExample)
