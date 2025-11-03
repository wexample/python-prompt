from __future__ import annotations

from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class EchoExample(AbstractResponseExample):
    """Example usage of EchoPromptResponse with various formatting."""
    def example_class(self):
        from wexample_prompt.responses.echo_prompt_response import EchoPromptResponse

        return EchoPromptResponse.create_echo(
            message=self.get_test_message(),
        )

    def example_extended(self) -> None:
        self._class_with_methods.echo(self.get_test_message())

    def example_manager(self) -> None:
        self.io.echo(message=self.get_test_message())

    def get_test_message(self) -> str:
        return "Test echo message"

    def example_normal(self) -> None:
        """Normal echo without formatting."""
        self.io.echo(message="Simple echo message")

    def example_formatted(self) -> None:
        """Echo with color and bold formatting."""
        self.io.echo(message="@color:cyan{Cyan text}")
        self.io.echo(message="@color:yellow+bold{Bold yellow text}")
        self.io.echo(message="@🔵{Blue emoji} with @color:magenta+bold{mixed} @color:green{formatting}")

    def example_indented(self) -> None:
        """Echo with indentation."""
        # Normal indentation
        self.io.echo(message="Normal echo", indentation=0)
        self.io.echo(message="Indented echo (level 3)", indentation=3)
        self.io.echo(message="Indented echo (level 5)", indentation=5)
        
        # Colored indentation
        self.io.echo(message="@color:cyan{Colored echo with indentation}", indentation=3)
        self.io.echo(message="@🟢+bold{Emoji and bold with indentation}", indentation=5)

    def get_examples(self) -> list[dict[str, Any]]:
        """Get list of examples.

        Returns:
            List of example configurations
        """
        return [
            {
                "title": "Normal",
                "description": "Simple echo without formatting",
                "callback": self.example_normal,
            },
            {
                "title": "Formatted",
                "description": "Echo with colors and bold",
                "callback": self.example_formatted,
            },
            {
                "title": "Indented",
                "description": "Echo with various indentation levels",
                "callback": self.example_indented,
            },
        ]
