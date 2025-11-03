"""Interactive example for error messages - delegates to src example."""

from ..abstract_prompt_response_example import AbstractPromptResponseExample


class ErrorExample(AbstractPromptResponseExample):
    """Interactive example for error messages with edge cases."""

    def execute(self) -> None:
        """Execute comprehensive error examples including edge cases."""
        from wexample_prompt.example.response.messages.error_example import (
            ErrorExample as SrcErrorExample,
        )

        demo_io = self.create_io_manager()
        src_example = SrcErrorExample()

        # Execute all examples from src
        for example_config in src_example.get_examples():
            demo_io.separator(f"@🔶{{{example_config['title']}}}")
            demo_io.log(f"  {example_config['description']}")
            if 'callback' in example_config:
                example_config['callback']()
