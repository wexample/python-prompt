"""Interactive example for list display - delegates to src example."""

from ..abstract_prompt_response_example import AbstractPromptResponseExample


class ListExample(AbstractPromptResponseExample):
    """Interactive example for list display."""

    def execute(self) -> None:
        """Execute list examples."""
        from wexample_prompt.example.response.data.list_example import (
            ListExample as SrcListExample,
        )

        demo_io = self.create_io_manager()
        src_example = SrcListExample()

        demo_io.log("@color:cyan{Basic list example}")
        src_example.example_manager()
