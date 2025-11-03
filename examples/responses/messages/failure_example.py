"""Interactive example for failure messages - delegates to src example."""

from ..abstract_prompt_response_example import AbstractPromptResponseExample


class FailureExample(AbstractPromptResponseExample):
    """Interactive example for failure messages."""

    def execute(self) -> None:
        """Execute failure examples."""
        from wexample_prompt.example.response.messages.failure_example import (
            FailureExample as SrcFailureExample,
        )

        demo_io = self.create_io_manager()
        src_example = SrcFailureExample()

        demo_io.separator("@🔴+bold{Failure Examples}")

        demo_io.log("@color:cyan{Basic failure example}")
        src_example.example_manager()

        demo_io.success("@🟢+bold{Failure examples complete}")
