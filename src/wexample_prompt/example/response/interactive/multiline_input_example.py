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

    def example_custom_prefix(self) -> None:
        response = self.io.multiline_input(
            question="Notes for today:",
            prompt_prefix="📝 ",
        )
        self._echo(response.get_value())

    def example_chatty(self) -> None:
        """Mimic a chat-session look: past turns + bordered input + footer hint."""
        io = self.io

        # Past turns (scripted) — neutral gray via io.log default.
        io.log("❯ Salut mon poulet")
        io.log("")
        io.log("● Salut ! 🐔 Qu'est-ce qu'on fait aujourd'hui ?")
        io.log("")
        io.log("✻ Worked for 2s")
        io.log("")
        io.log("❯ On fait juste des tests de conversation")
        io.log("")
        io.log(
            "● Ça marche, on teste tranquille. 😄 Vas-y, balance ce que tu veux — je réponds."
        )
        io.log("")
        io.log("✻ Cogitated for 3s")
        io.log("")

        response = io.multiline_input(
            question=None,
            prompt_prefix="❯ ",
            bordered=True,
            footer_hint="? for shortcuts · ← for agents",
        )

        value = response.get_value()
        if value is None:
            io.warning("Cancelled.")
            return
        io.log("")
        io.log(f"● You said: {value}")
        io.log("")
        io.log("✻ Replied in 1s")

    def _echo(self, value: str | None) -> None:
        if value is None:
            self.io.warning("Cancelled.")
            return
        self.io.frame(
            text=value.split("\n"),
            title="You typed",
        )

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
                "title": "Chatty",
                "description": "Chat-session look: past turns + bordered input + hint",
                "callback": self.example_chatty,
            },
        ]
