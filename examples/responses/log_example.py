"""Interactive example for log - delegates to src example."""

from .abstract_prompt_response_example import AbstractPromptResponseExample


class LogExample(AbstractPromptResponseExample):
    """Interactive example for log."""

    def execute(self) -> None:
        """Execute log examples."""
        from wexample_prompt.example.response.log_example import (
            LogExample as SrcLogExample,
        )

        demo_io = self.create_io_manager()
        src_example = SrcLogExample()

        demo_io.log("@color:cyan{Basic log example}")
        src_example.example_manager()
