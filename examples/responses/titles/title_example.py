"""Interactive example for title - delegates to src example."""

from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class TitleExample(AbstractPromptResponseExample):
    """Interactive example for title."""

    def execute(self) -> None:
        """Execute title examples."""
        from wexample_prompt.example.response.titles.title_example import (
            TitleExample as SrcTitleExample,
        )

        self.execute_delegated(SrcTitleExample)
