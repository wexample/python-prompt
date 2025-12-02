"""Interactive example for subtitle - delegates to src example."""

from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class SubtitleExample(AbstractPromptResponseExample):
    """Interactive example for subtitle."""

    def execute(self) -> None:
        """Execute subtitle examples."""
        from wexample_prompt.example.response.titles.subtitle_example import (
            SubtitleExample as SrcSubtitleExample,
        )

        self.execute_delegated(SrcSubtitleExample)
