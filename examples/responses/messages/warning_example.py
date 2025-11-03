"""Interactive example for warning messages - delegates to src example."""

from ..abstract_prompt_response_example import AbstractPromptResponseExample


class WarningExample(AbstractPromptResponseExample):
    """Interactive example for warning messages."""

    def execute(self) -> None:
        """Execute warning examples."""
        from wexample_prompt.example.response.messages.warning_example import (
            WarningExample as SrcWarningExample,
        )

        demo_io = self.create_io_manager()
        src_example = SrcWarningExample()

        demo_io.separator("@🟠+bold{Warning Examples}")

        demo_io.log("@color:cyan{Basic warning example}")
        src_example.example_manager()

        demo_io.success("@🟢+bold{Warning examples complete}")
