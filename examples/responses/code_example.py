"""Interactive example for code - delegates to src example."""

from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class CodeExample(AbstractPromptResponseExample):
    """Interactive example for code."""

    def execute(self) -> None:
        """Execute code examples."""
        from wexample_prompt.example.response.code_example import (
            CodeExample as SrcCodeExample,
        )

        self.execute_delegated(SrcCodeExample)
