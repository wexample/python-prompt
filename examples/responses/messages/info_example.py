"""Interactive example for info messages - delegates to src example."""

from ..abstract_prompt_response_example import AbstractPromptResponseExample


class InfoExample(AbstractPromptResponseExample):
    """Interactive example for info messages."""

    def execute(self) -> None:
        """Execute info examples."""
        from wexample_prompt.example.response.messages.info_example import (
            InfoExample as SrcInfoExample,
        )

        demo_io = self.create_io_manager()
        src_example = SrcInfoExample()

        demo_io.separator("@🔵+bold{Info Examples}")

        demo_io.log("@color:cyan{Basic info example}")
        src_example.example_manager()

        demo_io.success("@🟢+bold{Info examples complete}")
