"""Interactive example for table display - delegates to src example."""

from ..abstract_prompt_response_example import AbstractPromptResponseExample


class TableExample(AbstractPromptResponseExample):
    """Interactive example for table display."""

    def execute(self) -> None:
        """Execute table examples."""
        from wexample_prompt.example.response.data.table_example import (
            TableExample as SrcTableExample,
        )

        demo_io = self.create_io_manager()
        src_example = SrcTableExample()

        demo_io.log("@color:cyan{Basic table example}")
        src_example.example_manager()
