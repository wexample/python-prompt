"""Interactive example for multiple responses - delegates to src example."""

from ..abstract_prompt_response_example import AbstractPromptResponseExample


class MultipleExample(AbstractPromptResponseExample):
    """Interactive example for multiple responses."""

    def execute(self) -> None:
        """Execute multiple examples."""
        from wexample_prompt.example.response.data.multiple_example import (
            MultipleExample as SrcMultipleExample,
        )

        demo_io = self.create_io_manager()
        src_example = SrcMultipleExample()

        demo_io.separator("@🔵+bold{Multiple Examples}")

        # Execute all examples from src if available
        if hasattr(src_example, 'get_examples'):
            for example_config in src_example.get_examples():
                demo_io.separator(f"@🔶{{{example_config['title']}}}")
                demo_io.log(f"  {example_config['description']}")
                if 'callback' in example_config:
                    example_config['callback']()
        else:
            demo_io.log("@color:cyan{Basic multiple example}")
            src_example.example_manager()

        demo_io.success("@🟢+bold{Multiple examples complete}")
