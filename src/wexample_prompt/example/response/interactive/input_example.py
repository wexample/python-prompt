"""Example usage of InputPromptResponse."""

from __future__ import annotations

from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class InputExample(AbstractResponseExample):
    """Example usage of free-text input prompt responses."""

    def example_simple(self) -> None:
        """Simple text input."""
        self.io.input(
            question="Enter your name:",
            predefined_answer="Alice",
        )

    def example_with_default(self) -> None:
        """Text input with a pre-filled default value."""
        self.io.input(
            question="Enter the public URL:",
            default_value="https://api.myapp.com",
            predefined_answer="https://api.myapp.com",
        )

    def example_class(self, indentation: int | None = None):
        """Use the response class directly."""
        from wexample_prompt.responses.interactive.input_prompt_response import (
            InputPromptResponse,
        )

        return InputPromptResponse.create_input(
            question="Enter a value:",
            predefined_answer="test-value",
        )

    def example_manager(self) -> None:
        """Use IoManager mixin method."""
        self.io.input(
            question="Project name:",
            predefined_answer="my-project",
        )

    def get_examples(self) -> list[dict[str, Any]]:
        return [
            {
                "title": "Simple",
                "description": "Simple free-text input",
                "callback": self.example_simple,
            },
            {
                "title": "With Default",
                "description": "Text input with a pre-filled default value",
                "callback": self.example_with_default,
            },
        ]
