"""Interactive example for file picker - delegates to src example."""

from ..abstract_prompt_response_example import AbstractPromptResponseExample


class FilePickerExample(AbstractPromptResponseExample):
    """Interactive example for file picker."""

    def execute(self) -> None:
        """Execute file picker examples."""
        from wexample_prompt.example.response.interactive.file_picker_example import (
            FilePickerExample as SrcFilePickerExample,
        )

        demo_io = self.create_io_manager()
        src_example = SrcFilePickerExample()

        demo_io.log("@color:cyan{Basic file picker example}")
        src_example.example_manager()
