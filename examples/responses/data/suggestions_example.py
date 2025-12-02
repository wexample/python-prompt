"""Interactive example for suggestions - delegates to src example."""

from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class SuggestionsExample(AbstractPromptResponseExample):
    """Interactive example for suggestions."""

    def execute(self) -> None:
        """Execute suggestions examples."""
        from wexample_prompt.example.response.data.suggestions_example import (
            SuggestionsExample as SrcSuggestionsExample,
        )

        self.execute_delegated(SrcSuggestionsExample)
