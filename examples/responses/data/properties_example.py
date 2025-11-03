"""Interactive example for properties display - delegates to src example."""

from ..abstract_prompt_response_example import AbstractPromptResponseExample


class PropertiesExample(AbstractPromptResponseExample):
    """Interactive example for properties display."""

    def execute(self) -> None:
        """Execute properties examples."""
        from wexample_prompt.example.response.data.properties_example import (
            PropertiesExample as SrcPropertiesExample,
        )

        demo_io = self.create_io_manager()
        src_example = SrcPropertiesExample()

        demo_io.log("@color:cyan{Basic properties example}")
        src_example.example_manager()
