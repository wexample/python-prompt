"""Interactive example for echo - delegates to src example."""

from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class EchoExample(AbstractPromptResponseExample):
    """Interactive example for echo."""

    def execute(self) -> None:
        """Execute echo examples."""
        from wexample_prompt.example.response.echo_example import (
            EchoExample as SrcEchoExample,
        )

        self.execute_delegated(SrcEchoExample)
