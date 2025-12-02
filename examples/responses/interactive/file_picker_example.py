"""Interactive example for file picker - delegates to src example."""

from examples.responses.abstract_prompt_response_example import AbstractPromptResponseExample


class FilePickerExample(AbstractPromptResponseExample):
    """Interactive example for file picker."""

    def execute(self) -> None:
        """Execute file picker examples."""
        from wexample_prompt.example.response.interactive.file_picker_example import (
            FilePickerExample as SrcFilePickerExample,
        )

        self.execute_delegated(SrcFilePickerExample)
