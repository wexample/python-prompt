"""Example usage of ConfirmPromptResponse."""

from __future__ import annotations

from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class ConfirmExample(AbstractResponseExample):
    """Example usage of confirmation dialog responses."""

    @staticmethod
    def generate_long_paragraph() -> str:
        """Generate long paragraph for testing."""
        return (
            "@color:cyan+bold{This is a long paragraph} used to test how confirmation prompts behave when "
            "the question spans multiple lines. It contains enough words to exceed a "
            "@🔶{typical terminal width}, ensuring that auto-wrapping occurs."
        )

    @staticmethod
    def generate_long_url() -> str:
        """Generate long URL."""
        return (
            "https://example.com/some/really/long/path/that/keeps/going/and/going/"
            "and/contains/query?with=lots&of=parameters&and=maybe#fragments"
        )

    @staticmethod
    def generate_long_path() -> str:
        """Generate long file path."""
        return (
            "/home/user/projects/some_project/build/output/deploy/"
            "very/very/very/long/subdirectory/structure/with/files/and/more/files/"
            "and/even/more/nested/paths/that/should/wrap/properly.txt"
        )

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

    def edge_case_limits(self) -> None:
        """Test edge cases: limits (long text)."""
        from wexample_prompt.responses.interactive.confirm_prompt_response import (
            ConfirmPromptResponse,
        )

        # Long paragraph
        self.io.confirm(
            question=self.generate_long_paragraph(),
            choices=ConfirmPromptResponse.MAPPING_PRESET_YES_NO,
            default="yes",
            reset_on_finish=True,
            predefined_answer="yes",
        )

        # Long URL
        self.io.confirm(
            question=f"Open this @🔷+bold{{URL}}? {self.generate_long_url()}",
            choices=ConfirmPromptResponse.MAPPING_PRESET_OK_CANCEL,
            default="ok",
            reset_on_finish=True,
            predefined_answer="ok",
        )

        # Long path
        self.io.confirm(
            question=f"Use this @color:yellow+bold{{file path}}? {self.generate_long_path()}",
            choices=ConfirmPromptResponse.MAPPING_PRESET_OK_CANCEL,
            default="ok",
            reset_on_finish=True,
            predefined_answer="ok",
        )

    def edge_case_indentation(self) -> None:
        """Test edge cases: indentation."""
        from wexample_prompt.responses.interactive.confirm_prompt_response import (
            ConfirmPromptResponse,
        )

        self.io.confirm(
            question="@🟢+bold{Confirm with indentation}",
            choices=ConfirmPromptResponse.MAPPING_PRESET_YES_NO,
            default="yes",
            reset_on_finish=True,
            indentation=5,
            predefined_answer="yes",
        )

        self.io.indentation = 5
        self.io.confirm(
            question="@🟢+bold{Confirm with double indentation}",
            choices=ConfirmPromptResponse.MAPPING_PRESET_YES_NO,
            default="yes",
            reset_on_finish=True,
            indentation=5,
            predefined_answer="yes",
        )
        self.io.indentation = 0

    def edge_case_nesting(self) -> None:
        """Test edge cases: nesting."""
        from wexample_prompt.responses.interactive.confirm_prompt_response import (
            ConfirmPromptResponse,
        )

        # Simulated nested confirmations
        self.io.confirm(
            question="@🔵+bold{Level 1: Proceed?}",
            choices=ConfirmPromptResponse.MAPPING_PRESET_YES_NO,
            default="yes",
            reset_on_finish=True,
            predefined_answer="yes",
        )

        self.io.indentation += 1
        self.io.confirm(
            question="@🟠+bold{Level 2: Are you sure?}",
            choices=ConfirmPromptResponse.MAPPING_PRESET_YES_NO,
            default="no",
            reset_on_finish=True,
            predefined_answer="yes",
        )

        self.io.indentation += 1
        self.io.confirm(
            question="@🔴+bold{Level 3: Final confirmation}",
            choices=ConfirmPromptResponse.MAPPING_PRESET_OK_CANCEL,
            default="cancel",
            reset_on_finish=True,
            predefined_answer="ok",
        )
        self.io.indentation = 0

    def get_examples(self) -> list[dict[str, Any]]:
        """Get list of examples.

        Returns:
            List of example configurations
        """
        return [
            {
                "title": "Basic Confirm",
                "description": "Simple confirmation dialog",
                "callback": self.example_manager,
            },
            {
                "title": "Edge Case: Limits",
                "description": "Long text, URLs, and paths",
                "callback": self.edge_case_limits,
            },
            {
                "title": "Edge Case: Indentation",
                "description": "Confirmations with various indentation levels",
                "callback": self.edge_case_indentation,
            },
            {
                "title": "Edge Case: Nesting",
                "description": "Nested confirmation dialogs",
                "callback": self.edge_case_nesting,
            },
        ]
