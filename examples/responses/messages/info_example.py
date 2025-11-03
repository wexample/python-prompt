"""Interactive example for info - delegates to src example."""

from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class InfoExample(AbstractPromptResponseExample):
    """Interactive example for info."""

    def execute(self) -> None:
        """Execute info examples."""
        from wexample_prompt.example.response.messages.info_example import (
            InfoExample as SrcInfoExample,
        )

        self.execute_delegated(SrcInfoExample)
