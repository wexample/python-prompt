"""Interactive example for choice prompts - delegates to src example."""

from ..abstract_prompt_response_example import AbstractPromptResponseExample


class ChoiceExample(AbstractPromptResponseExample):
    """Interactive example for choice prompts with edge cases."""

    def execute(self) -> None:
        """Execute comprehensive choice examples including edge cases."""
        from wexample_prompt.example.response.interactive.choice_example import (
            ChoiceExample as SrcChoiceExample,
        )

        demo_io = self.create_io_manager()
        src_example = SrcChoiceExample()

        # Execute all examples from src
        for example_config in src_example.get_examples():
            demo_io.separator(f"@🔶{{{example_config['title']}}}")
            demo_io.log(f"  {example_config['description']}")
            if 'callback' in example_config:
                example_config['callback']()
