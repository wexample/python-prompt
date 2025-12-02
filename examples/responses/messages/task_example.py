"""Interactive example for task - delegates to src example."""

from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class TaskExample(AbstractPromptResponseExample):
    """Interactive example for task."""

    def execute(self) -> None:
        """Execute task examples."""
        from wexample_prompt.example.response.messages.task_example import (
            TaskExample as SrcTaskExample,
        )

        self.execute_delegated(SrcTaskExample)
