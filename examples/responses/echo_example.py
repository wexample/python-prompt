"""Interactive example for echo - delegates to src example."""

from .abstract_prompt_response_example import AbstractPromptResponseExample


class EchoExample(AbstractPromptResponseExample):
    """Interactive example for echo."""

    def execute(self) -> None:
        """Execute echo examples."""
        from wexample_prompt.example.response.echo_example import (
            EchoExample as SrcEchoExample,
        )

        demo_io = self.create_io_manager()
        src_example = SrcEchoExample()

        demo_io.log("@color:cyan{Basic echo example}")
        src_example.example_manager()
