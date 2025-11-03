from __future__ import annotations

from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class ChoiceExample(AbstractResponseExample):
    """Example usage of ChoicePromptResponse with edge cases."""

    @staticmethod
    def generate_long_multiline_text() -> str:
        """Generate long multiline text for testing limits."""
        several_lines = "> @color:cyan{And several short lines}\n"
        return (
            "@🔵+bold{This is a }" + ("@color:yellow{long} " * 15) + "text\n"
            "> With a " + ("@color:magenta{long} " * 10) + "line\n"
            + several_lines * 10
        )

    @staticmethod
    def generate_long_single_line_text() -> str:
        """Generate long single line text for testing wrapping."""
        return (
            "@🔵+bold{This is a }"
            + ("@color:yellow{long} " * 20)
            + "text with @🟣+underline{inline styling} sprinkled everywhere."
        )

    @staticmethod
    def generate_special_characters_text() -> str:
        """Generate text with special characters."""
        return "@🔵{Special: } émojis 🎉 symbols ±×÷ quotes \"'` brackets []{}() slashes /\\"
    def example_class(self, indentation: int | None = None):
        from wexample_prompt.responses.interactive.choice_prompt_response import (
            ChoicePromptResponse,
        )

        return ChoicePromptResponse.create_choice(
            question="Select an option:",
            choices={
                "value1": "Choice 1",
                "value2": "Choice 2",
                "value3": "Choice 3",
            },
            default="value2",
            predefined_answer="value3",
        )

    def example_extended(self) -> None:
        choices = ["Option 1", "Option 2", "Option 3"]
        self._class_with_methods.choice(
            question="Select an option:", choices=choices, predefined_answer="Option 2"
        )

    def example_manager(self) -> None:
        choices = ["Option 1", "Option 2", "Option 3"]
        self.io.choice(
            question="Select an option:", choices=choices, predefined_answer="Option 2"
        )

    def edge_case_limits(self) -> None:
        """Test edge cases: limits (long text, many choices)."""
        # Long multiline text
        self.io.choice(
            question=self.generate_long_multiline_text(),
            choices=["Option A", "Option B"],
            predefined_answer="Option A",
        )

        # Long single line
        self.io.choice(
            question=self.generate_long_single_line_text(),
            choices=["Yes", "No"],
            predefined_answer="Yes",
        )

        # Very long choice labels
        self.io.choice(
            question="Select an option with @🔵+bold{very long labels}:",
            choices=[
                "This is a very long choice label that contains a lot of text and should test wrapping",
                "Another extremely long option with lots of words",
                "Short",
            ],
            predefined_answer="Short",
        )

        # Many choices
        many_choices = {f"option_{i}": f"Option {i}" for i in range(1, 21)}
        self.io.choice(
            question="Select from @🔵+bold{many options}:",
            choices=many_choices,
            predefined_answer="option_1",
        )

    def edge_case_indentation(self) -> None:
        """Test edge cases: indentation."""
        self.io.choice(
            question="@🟢+bold{Choice with indentation}",
            choices=["Yes", "No"],
            indentation=5,
            predefined_answer="Yes",
        )

        self.io.indentation = 3
        self.io.choice(
            question="@🟢+bold{Choice with double indentation}",
            choices=["Yes", "No"],
            indentation=5,
            predefined_answer="Yes",
        )
        self.io.indentation = 0

    def edge_case_special(self) -> None:
        """Test edge cases: special characters."""
        self.io.choice(
            question=self.generate_special_characters_text(),
            choices=[
                "Option with émojis 🎉",
                "Option with symbols ±×÷",
                "Normal option",
            ],
            predefined_answer="Normal option",
        )

    def get_examples(self) -> list[dict[str, Any]]:
        """Get list of examples.

        Returns:
            List of example configurations
        """
        return [
            {
                "title": "Basic Choice",
                "description": "Simple choice with predefined answer",
                "callback": self.example_manager,
            },
            {
                "title": "Edge Case: Limits",
                "description": "Long text and many choices",
                "callback": self.edge_case_limits,
            },
            {
                "title": "Edge Case: Indentation",
                "description": "Choices with various indentation levels",
                "callback": self.edge_case_indentation,
            },
            {
                "title": "Edge Case: Special Characters",
                "description": "Choices with unicode and special characters",
                "callback": self.edge_case_special,
            },
        ]
