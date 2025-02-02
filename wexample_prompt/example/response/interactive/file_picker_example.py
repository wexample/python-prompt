"""Example usage of FilePickerPromptResponse."""
from typing import List, Any, Dict, Optional

from wexample_prompt.example.abstract_response_example import AbstractResponseExample
from wexample_prompt.responses.interactive.file_picker_prompt_response import FilePickerPromptResponse


class FilePickerExample(AbstractResponseExample):
    """Example usage of FilePickerPromptResponse."""

    @classmethod
    def get_response_class(cls) -> type:
        """Get the response class this example is for.

        Returns:
            Type: The response class
        """
        return FilePickerPromptResponse

    def get_examples(self) -> List[Dict[str, Any]]:
        """Get list of examples.

        Returns:
            List[Dict[str, Any]]: List of example configurations
        """
        return [
            {
                "title": "Simple File Picker",
                "description": "Display a file picker in current directory",
                "callback": self.simple_file_picker
            },
            {
                "title": "Custom Question",
                "description": "File picker with custom question",
                "callback": self.custom_question
            },
            {
                "title": "Custom Base Directory",
                "description": "File picker starting in a specific directory",
                "callback": self.custom_base_dir
            }
        ]

    def simple_file_picker(self) -> Optional[FilePickerPromptResponse]:
        """Show a simple file picker example."""
        return self.io_manager.file_picker()

    def custom_question(self) -> Optional[FilePickerPromptResponse]:
        """Show a file picker with custom question."""
        return self.io_manager.file_picker(
            question="Please select a configuration file:"
        )

    def custom_base_dir(self) -> Optional[FilePickerPromptResponse]:
        """Show a file picker with custom base directory."""
        return self.io_manager.file_picker(
            base_dir="/etc",
            question="Select a system configuration file:"
        )
