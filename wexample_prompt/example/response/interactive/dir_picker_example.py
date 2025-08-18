"""Example usage of DirPickerPromptResponse."""

from typing import Optional

from wexample_prompt.example.abstract_response_example import AbstractResponseExample
from wexample_prompt.responses.interactive.dir_picker_prompt_response import DirPickerPromptResponse


class DirPickerExample(AbstractResponseExample):

    def example_class(self, indentation: Optional[int] = None):
        return DirPickerPromptResponse.create_dir_picker(
            question="Select a directory:",
            base_dir=None,  # Will use current working directory
        )

    def example_manager(self):
        self.io.dir_picker("Select a directory:")

    def example_extended(self):
        self._class_with_methods.dir_picker("Select a directory:")
