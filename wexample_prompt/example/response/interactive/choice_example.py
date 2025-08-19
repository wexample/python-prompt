from typing import Optional

from wexample_prompt.example.abstract_response_example import AbstractResponseExample
from wexample_prompt.responses.interactive.choice_prompt_response import ChoicePromptResponse


class ChoiceExample(AbstractResponseExample):

    def example_class(self, indentation: Optional[int] = None):
        return ChoicePromptResponse.create_choice(
            question="Select an option:",
            choices={
                "value1": "Choice 1",
                "value2": "Choice 2",
                "value3": "Choice 3",
            },
        )

    def example_manager(self):
        choices = ["Option 1", "Option 2", "Option 3"]
        self.io.choice("Select an option:", choices)

    def example_extended(self):
        choices = ["Option 1", "Option 2", "Option 3"]
        self._class_with_methods.choice("Select an option:", choices)
