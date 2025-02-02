"""Example usage of DirPickerPromptResponse."""
from wexample_prompt.responses.interactive.dir_picker_prompt_response import DirPickerPromptResponse


class DirPickerExample:
    """Example class demonstrating DirPickerPromptResponse usage."""

    @classmethod
    def get_example(cls) -> DirPickerPromptResponse:
        """Get an example DirPickerPromptResponse.

        Returns:
            DirPickerPromptResponse: An example response
        """
        return DirPickerPromptResponse.create_dir_picker(
            question="Select a directory to process:",
            abort="Cancel"
        )
