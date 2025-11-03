"""Interactive example for separator - delegates to src example."""

from ..abstract_prompt_response_example import AbstractPromptResponseExample


class SeparatorExample(AbstractPromptResponseExample):
    """Interactive example for separator."""

    def execute(self) -> None:
        """Execute separator examples."""
        from wexample_prompt.example.response.titles.separator_example import (
            SeparatorExample as SrcSeparatorExample,
        )

        demo_io = self.create_io_manager()
        src_example = SrcSeparatorExample()

        demo_io.separator("@🔵+bold{Separator Examples}")

        demo_io.log("@color:cyan{Basic separator example}")
        src_example.example_manager()

        demo_io.success("@🟢+bold{Separator examples complete}")
