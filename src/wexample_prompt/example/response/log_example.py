from __future__ import annotations

from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class LogExample(AbstractResponseExample):
    """Example usage of LogPromptResponse with various formatting."""
    def example_class(self):
        from wexample_prompt.responses.log_prompt_response import LogPromptResponse

        return LogPromptResponse.create_log(
            message=self.get_test_message(),
        )

    def example_extended(self) -> None:
        self._class_with_methods.log(message=self.get_test_message())

    def example_manager(self) -> None:
        self.io.log(message=self.get_test_message())

    def get_test_message(self) -> str:
        return "Test log message"

    def example_normal(self) -> None:
        """Normal log without formatting."""
        self.io.log(message="Simple log message")

    def example_formatted(self) -> None:
        """Log with color and bold formatting."""
        self.io.log(message="@color:cyan{Cyan log}")
        self.io.log(message="@color:yellow+bold{Bold yellow log}")
        self.io.log(message="@🔵{Blue emoji} with @color:magenta+bold{mixed} @color:green{formatting}")

    def example_indented(self) -> None:
        """Log with indentation."""
        # Normal indentation
        self.io.log(message="Normal log", indentation=0)
        self.io.log(message="Indented log (level 3)", indentation=3)
        self.io.log(message="Indented log (level 5)", indentation=5)
        
        # Colored indentation
        self.io.log(message="@color:cyan{Colored log with indentation}", indentation=3)
        self.io.log(message="@🟢+bold{Emoji and bold with indentation}", indentation=5)

    def get_examples(self) -> list[dict[str, Any]]:
        """Get list of examples.

        Returns:
            List of example configurations
        """
        return [
            {
                "title": "Normal",
                "description": "Simple log without formatting",
                "callback": self.example_normal,
            },
            {
                "title": "Formatted",
                "description": "Log with colors and bold",
                "callback": self.example_formatted,
            },
            {
                "title": "Indented",
                "description": "Log with various indentation levels",
                "callback": self.example_indented,
            },
        ]
