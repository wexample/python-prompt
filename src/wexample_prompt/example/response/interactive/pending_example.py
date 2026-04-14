from __future__ import annotations

from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class PendingExample(AbstractResponseExample):
    """Example usage of PendingPromptResponse."""

    def demo_service_startup(self) -> None:
        """Simulate waiting for a database service, showing raw subprocess-style output."""
        import subprocess

        attempts = {"n": 0, "max": 4}

        def _check() -> tuple[bool, list[str]]:
            attempts["n"] += 1
            result = subprocess.run(
                [
                    "echo",
                    f"psql: error: could not connect to server (attempt {attempts['n']})",
                ],
                capture_output=True,
                text=True,
            )
            lines = result.stdout.strip().splitlines()
            return attempts["n"] >= attempts["max"], lines

        self.io.pending(
            callback=_check,
            label="Waiting for postgres to start...",
            interval=0.2,
            max_lines=3,
        )

    def example_class(self):
        from wexample_prompt.responses.interactive.pending_prompt_response import (
            PendingPromptResponse,
        )

        counter = {"n": 0}

        def _check() -> tuple[bool, list[str]]:
            counter["n"] += 1
            lines = [f"Attempt {counter['n']}: connection refused (simulated)"]
            return counter["n"] >= 3, lines

        return PendingPromptResponse.create_pending(
            callback=_check,
            label="Waiting for service...",
            interval=0.3,
        )

    def example_extended(self) -> None:
        counter = {"n": 0}

        def _check() -> tuple[bool, list[str]]:
            counter["n"] += 1
            lines = [f"Attempt {counter['n']}: connection refused (simulated)"]
            return counter["n"] >= 3, lines

        self._class_with_methods.pending(
            callback=_check,
            label="Waiting for service... (extended)",
            interval=0.3,
        )

    def example_manager(self) -> None:
        counter = {"n": 0}

        def _check() -> tuple[bool, list[str]]:
            counter["n"] += 1
            lines = [f"Attempt {counter['n']}: connection refused (simulated)"]
            return counter["n"] >= 3, lines

        self.io.pending(
            callback=_check,
            label="Waiting for service...",
            interval=0.3,
        )

    def get_examples(self) -> list[dict[str, Any]]:
        return [
            {
                "title": "Basic Pending",
                "description": "Simple poll with simulated output lines",
                "callback": self.example_manager,
            },
            {
                "title": "Service Startup Simulation",
                "description": "Simulate waiting for a database, showing subprocess output",
                "callback": self.demo_service_startup,
            },
        ]
