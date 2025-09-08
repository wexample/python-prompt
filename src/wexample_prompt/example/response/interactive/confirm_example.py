"""Example usage of ConfirmPromptResponse."""

from __future__ import annotations

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


class ConfirmExample(AbstractResponseExample):
    """Example usage of confirmation dialog responses."""
    def example_class(self, indentation: int | None = None):
        """Use the response class directly."""
        from wexample_prompt.responses.interactive.confirm_prompt_response import (
            ConfirmPromptResponse,
        )

        return ConfirmPromptResponse.create_confirm(
            question="Proceed?",
            choices=ConfirmPromptResponse.MAPPING_PRESET_YES_NO_ALL,
            reset_on_finish=True,
            predefined_answer="yes",
        )

    def example_extended(self) -> None:
        """Use extended context with _class_with_methods."""
        from wexample_prompt.responses.interactive.confirm_prompt_response import (
            ConfirmPromptResponse,
        )

        self._class_with_methods.confirm(
            question="Proceed?",
            choices=ConfirmPromptResponse.MAPPING_PRESET_YES_NO_ALL,
            reset_on_finish=True,
            predefined_answer="no",
        )

    def example_manager(self) -> None:
        """Use IoManager mixin method."""
        from wexample_prompt.responses.interactive.confirm_prompt_response import (
            ConfirmPromptResponse,
        )

        self.io.confirm(
            question="Proceed?",
            choices=ConfirmPromptResponse.MAPPING_PRESET_OK_CANCEL,
            reset_on_finish=True,
            predefined_answer="cancel",
        )
