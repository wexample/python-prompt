"""Abstract base class for simple message examples (echo, log, info, debug, etc.)."""

from __future__ import annotations

from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class AbstractSimpleMessageExample(AbstractResponseExample):
    """Base class for simple message examples with standard formatting tests."""

    def example_normal(self) -> None:
        """Normal message without formatting."""
        method = self.get_io_method()
        name = self.get_response_name()
        method(message=f"Simple {name} message")

    def example_formatted(self) -> None:
        """Message with color and bold formatting."""
        method = self.get_io_method()
        method(message="@color:cyan{Cyan text}")
        method(message="@color:yellow+bold{Bold yellow text}")
        method(message="@🔵{Blue emoji} with @color:magenta+bold{mixed} @color:green{formatting}")

    def example_indented(self) -> None:
        """Message with indentation."""
        method = self.get_io_method()
        name = self.get_response_name()
        
        # Normal indentation
        method(message=f"Normal {name}", indentation=0)
        method(message=f"Indented {name} (level 3)", indentation=3)
        method(message=f"Indented {name} (level 5)", indentation=5)
        
        # Colored indentation
        method(message=f"@color:cyan{{Colored {name} with indentation}}", indentation=3)
        method(message=f"@🟢+bold{{Emoji and bold {name} with indentation}}", indentation=5)

    def get_examples(self) -> list[dict[str, Any]]:
        """Get list of examples.

        Returns:
            List of example configurations
        """
        return [
            {
                "title": "Normal",
                "description": "Simple message without formatting",
                "callback": self.example_normal,
            },
            {
                "title": "Formatted",
                "description": "Message with colors and bold",
                "callback": self.example_formatted,
            },
            {
                "title": "Indented",
                "description": "Message with various indentation levels",
                "callback": self.example_indented,
            },
        ]
