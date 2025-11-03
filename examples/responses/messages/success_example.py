"""Interactive example for success messages - delegates to src example."""

from ..abstract_prompt_response_example import AbstractPromptResponseExample


class SuccessExample(AbstractPromptResponseExample):
    """Interactive example for success messages."""

    def execute(self) -> None:
        """Execute success examples."""
        from wexample_prompt.example.response.messages.success_example import (
            SuccessExample as SrcSuccessExample,
        )

        demo_io = self.create_io_manager()
        src_example = SrcSuccessExample()

        demo_io.log("@color:cyan{Basic success example}")
        src_example.example_manager()
