"""Interactive example for progress bars - delegates to src example."""

from ..abstract_prompt_response_example import AbstractPromptResponseExample


class ProgressExample(AbstractPromptResponseExample):
    """Interactive example for progress bars with edge cases."""

    def execute(self) -> None:
        """Execute comprehensive progress examples including edge cases."""
        from wexample_prompt.example.response.interactive.progress_example import (
            ProgressExample as SrcProgressExample,
        )

        demo_io = self.create_io_manager()
        src_example = SrcProgressExample()

        demo_io.separator("@🔵+bold{Progress Examples - All Cases}")

        # Execute all examples from src
        for example_config in src_example.get_examples():
            demo_io.separator(f"@🔶{{{example_config['title']}}}")
            demo_io.log(f"  {example_config['description']}")
            if 'callback' in example_config:
                example_config['callback']()

        demo_io.success("@🟢+bold{Progress examples complete}")
