"""Interactive example for debug messages - delegates to src example."""

from ..abstract_prompt_response_example import AbstractPromptResponseExample


class DebugExample(AbstractPromptResponseExample):
    """Interactive example for debug messages."""

    def execute(self) -> None:
        """Execute debug examples."""
        from wexample_prompt.example.response.messages.debug_example import (
            DebugExample as SrcDebugExample,
        )

        demo_io = self.create_io_manager()
        src_example = SrcDebugExample()

        demo_io.log("@color:cyan{Basic debug example}")
        src_example.example_manager()
