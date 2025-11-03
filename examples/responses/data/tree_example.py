"""Interactive example for tree display - delegates to src example."""

from ..abstract_prompt_response_example import AbstractPromptResponseExample


class TreeExample(AbstractPromptResponseExample):
    """Interactive example for tree display."""

    def execute(self) -> None:
        """Execute tree examples."""
        from wexample_prompt.example.response.data.tree_example import (
            TreeExample as SrcTreeExample,
        )

        demo_io = self.create_io_manager()
        src_example = SrcTreeExample()

        demo_io.separator("@🔵+bold{Tree Examples}")

        demo_io.log("@color:cyan{Basic tree example}")
        src_example.example_manager()

        demo_io.success("@🟢+bold{Tree examples complete}")
