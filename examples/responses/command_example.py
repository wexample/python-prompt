"""Interactive example for command - delegates to src example."""

from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class CommandExample(AbstractPromptResponseExample):
    """Interactive example for command."""

    def execute(self) -> None:
        """Execute command examples."""
        from wexample_prompt.example.response.command_example import (
            CommandExample as SrcCommandExample,
        )

        self.execute_delegated(SrcCommandExample)
