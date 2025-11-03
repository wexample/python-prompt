"""Interactive example for title - delegates to src example."""

from ..abstract_prompt_response_example import AbstractPromptResponseExample


class TitleExample(AbstractPromptResponseExample):
    """Interactive example for title."""

    def execute(self) -> None:
        """Execute title examples."""
        from wexample_prompt.example.response.titles.title_example import (
            TitleExample as SrcTitleExample,
        )

        demo_io = self.create_io_manager()
        src_example = SrcTitleExample()

        demo_io.separator("@🔵+bold{Title Examples}")

        demo_io.log("@color:cyan{Basic title example}")
        src_example.example_manager()

        demo_io.success("@🟢+bold{Title examples complete}")
