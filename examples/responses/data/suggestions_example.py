"""Interactive example for suggestions display - delegates to src example."""

from ..abstract_prompt_response_example import AbstractPromptResponseExample


class SuggestionsExample(AbstractPromptResponseExample):
    """Interactive example for suggestions display."""

    def execute(self) -> None:
        """Execute suggestions examples."""
        from wexample_prompt.example.response.data.suggestions_example import (
            SuggestionsExample as SrcSuggestionsExample,
        )

        demo_io = self.create_io_manager()
        src_example = SrcSuggestionsExample()

        demo_io.log("@color:cyan{Basic suggestions example}")
        src_example.example_manager()
