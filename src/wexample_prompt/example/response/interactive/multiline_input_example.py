from __future__ import annotations

from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class MultilineInputExample(AbstractResponseExample):
    """Example for the multi-line input response."""

    def example_class(self):
        from wexample_prompt.responses.interactive.multiline_input_prompt_response import (
            MultilineInputPromptResponse,
        )

        return MultilineInputPromptResponse.create_multiline_input(
            predefined_answer="hello\nworld",
        )

    def example_completions(self) -> None:
        response = self.io.multiline_input(
            question="Type / for commands:",
            bordered=True,
            footer_hint="? Type / to see commands · ↑↓ to navigate · Tab/Enter to accept",
            completions=[
                ("/add-dir", "Add a new working directory"),
                ("/advisor", "Configure the Advisor Tool"),
                ("/agents", "Manage agent configurations"),
                ("/autofix-pr", "Monitor and autofix issues with the current PR"),
                ("/help", "Show help"),
                ("/exit", "Quit the session"),
            ],
        )
        self._echo(response.get_value())

    def example_custom_prefix(self) -> None:
        response = self.io.multiline_input(
            question="Notes for today:",
            prompt_prefix="📝 ",
        )
        self._echo(response.get_value())

    def example_extended(self) -> None:
        response = self._class_with_methods.multiline_input(
            question="Write something (Esc+Enter for newline):",
        )
        self._echo(response.get_value())

    def example_manager(self) -> None:
        response = self.io.multiline_input(
            question="Write something (Esc+Enter for newline):",
        )
        self._echo(response.get_value())

    def example_with_default(self) -> None:
        response = self.io.multiline_input(
            question="Edit the draft below:",
            default_value="Hi there,\n\nThis is a draft message.",
        )
        self._echo(response.get_value())

    def get_examples(self) -> list[dict[str, Any]]:
        return [
            {
                "title": "Simple",
                "description": "Plain multi-line input then echo",
                "callback": self.example_manager,
            },
            {
                "title": "With default",
                "description": "Pre-fill with editable draft",
                "callback": self.example_with_default,
            },
            {
                "title": "Custom prefix",
                "description": "Replace the ❯ with an emoji",
                "callback": self.example_custom_prefix,
            },
            {
                "title": "Completions",
                "description": "Type / to trigger autocomplete in the info zone",
                "callback": self.example_completions,
            },
        ]

    def _echo(self, value: str | None) -> None:
        if value is None:
            self.io.warning("Cancelled.")
            return
        self.io.frame(
            text=value.split("\n"),
            title="You typed",
        )
