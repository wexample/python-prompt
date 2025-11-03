"""Interactive example for subtitle - delegates to src example."""

from ..abstract_prompt_response_example import AbstractPromptResponseExample


class SubtitleExample(AbstractPromptResponseExample):
    """Interactive example for subtitle."""

    def execute(self) -> None:
        """Execute subtitle examples."""
        from wexample_prompt.example.response.titles.subtitle_example import (
            SubtitleExample as SrcSubtitleExample,
        )

        demo_io = self.create_io_manager()
        src_example = SrcSubtitleExample()

        demo_io.log("@color:cyan{Basic subtitle example}")
        src_example.example_manager()
