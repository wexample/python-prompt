"""Example usage of ConfirmPromptResponse."""
from typing import Optional

from wexample_prompt.example.abstract_response_example import AbstractResponseExample
from wexample_prompt.responses.interactive.confirm_prompt_response import ConfirmPromptResponse


class ConfirmExample(AbstractResponseExample):
    """Example usage of confirmation dialog responses."""

    def example_class(self, indentation: Optional[int] = None):
        """Use the response class directly."""
        return ConfirmPromptResponse.create_confirm(
            question="Proceed?",
            preset="yes_no",
        )

    def example_manager(self):
        """Use IoManager mixin method."""
        self.io.confirm(question="Proceed?", preset="ok_cancel")

    def example_extended(self):
        """Use extended context with _class_with_methods."""
        self._class_with_methods.confirm(question="Proceed?", preset="yes_no_all")
