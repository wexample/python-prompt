"""Interactive example for frame - delegates to src example."""

from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class FrameExample(AbstractPromptResponseExample):
    """Interactive example for frame."""

    def execute(self) -> None:
        """Execute frame examples."""
        from wexample_prompt.example.response.frame_example import (
            FrameExample as SrcFrameExample,
        )

        self.execute_delegated(SrcFrameExample)
