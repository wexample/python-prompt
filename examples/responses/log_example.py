"""Interactive example for log - delegates to src example."""

from .abstract_prompt_response_example import AbstractPromptResponseExample


class LogExample(AbstractPromptResponseExample):
    """Interactive example for log."""

    def execute(self) -> None:
        """Execute log examples."""
        from wexample_prompt.example.response.log_example import (
            LogExample as SrcLogExample,
        )

        self.execute_delegated(SrcLogExample)
