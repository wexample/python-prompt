"""Interactive example for screen prompts - delegates to src example."""

from ..abstract_prompt_response_example import AbstractPromptResponseExample


class ScreenExample(AbstractPromptResponseExample):
    """Interactive example for screen prompts."""

    def execute(self) -> None:
        """Execute screen examples."""
        from wexample_prompt.example.response.interactive.screen_example import (
            ScreenExample as SrcScreenExample,
        )

        demo_io = self.create_io_manager()
        src_example = SrcScreenExample()

        demo_io.separator("@🔵+bold{Screen Examples}")

        # Execute basic examples from src
        demo_io.log("@color:cyan{Basic screen example}")
        src_example.example_manager()

        demo_io.success("@🟢+bold{Screen examples complete}")
