"""Interactive example for screen prompts - delegates to src example."""

from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class ScreenExample(AbstractPromptResponseExample):
    """Interactive example for screen prompts."""

    def execute(self) -> None:
        """Execute screen examples."""
        from wexample_prompt.example.response.interactive.screen_example import (
            ScreenExample as SrcScreenExample,
        )

        self.execute_delegated(SrcScreenExample)
