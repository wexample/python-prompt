"""Chat-session look: scripted past turns + bordered input + footer hint."""

from __future__ import annotations

from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class ChattyExample(AbstractResponseExample):
    """Demonstrate a Claude-style chat session built on top of multiline_input."""

    def example_class(self):
        from wexample_prompt.responses.interactive.multiline_input_prompt_response import (
            MultilineInputPromptResponse,
        )

        return MultilineInputPromptResponse.create_multiline_input(
            predefined_answer="(scripted)",
            bordered=True,
        )

    def example_extended(self) -> None:
        self.example_manager()

    def example_manager(self) -> None:
        io = self.io

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

    def get_examples(self) -> list[dict[str, Any]]:
        return [
            {
                "title": "Chatty",
                "description": "Past turns + bordered input + footer hint",
                "callback": self.example_manager,
            },
        ]
