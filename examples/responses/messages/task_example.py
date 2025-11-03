"""Interactive example for task messages - delegates to src example."""

from ..abstract_prompt_response_example import AbstractPromptResponseExample


class TaskExample(AbstractPromptResponseExample):
    """Interactive example for task messages."""

    def execute(self) -> None:
        """Execute task examples."""
        from wexample_prompt.example.response.messages.task_example import (
            TaskExample as SrcTaskExample,
        )

        demo_io = self.create_io_manager()
        src_example = SrcTaskExample()

        demo_io.log("@color:cyan{Basic task example}")
        src_example.example_manager()
