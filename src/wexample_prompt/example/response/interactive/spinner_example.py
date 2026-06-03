from __future__ import annotations

import time
from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class SpinnerExample(AbstractResponseExample):
    """Demo of the sticky bottom-line spinner."""

    def example_class(self):
        from wexample_prompt.responses.interactive.spinner_prompt_response import (
            SpinnerPromptResponse,
        )

        return SpinnerPromptResponse.create_spinner(label="Demo")

    def example_extended(self) -> None:
        self.example_manager()

    def example_manager(self) -> None:
        spinner = self.io.spinner(label="Thinking…")
        time.sleep(0.6)
        spinner.stop()

    def example_simulated_agent(self) -> None:
        import threading

        events: list[str] = []
        lock = threading.Lock()

        def worker() -> None:
            for label in ("Bash", "Read", "Edit", "Bash"):
                time.sleep(0.5)
                with lock:
                    events.append(f"$ {label}")

        spinner = self.io.spinner(label="Agent working…")
        t = threading.Thread(target=worker, daemon=True)
        t.start()

        seen = 0
        while t.is_alive():
            time.sleep(0.05)
            with lock:
                while seen < len(events):
                    spinner.log(events[seen])
                    seen += 1
        t.join()
        with lock:
            while seen < len(events):
                spinner.log(events[seen])
                seen += 1
        spinner.stop()

    def example_with_events(self) -> None:
        spinner = self.io.spinner(label="Thinking…")
        events = [
            "$ Bash: git log -1",
            "$ Read: src/wexample_prompt/responses/log_prompt_response.py",
            "$ Grep: spinner",
            "$ Bash: pytest -q",
        ]
        for ev in events:
            time.sleep(0.4)
            spinner.log(ev)
        time.sleep(0.4)
        spinner.stop()

    def get_examples(self) -> list[dict[str, Any]]:
        return [
            {
                "title": "Simple",
                "description": "Spinner that spins briefly then stops",
                "callback": self.example_manager,
            },
            {
                "title": "With events",
                "description": "Log persistent events above the spinner as it spins",
                "callback": self.example_with_events,
            },
            {
                "title": "Simulated agent",
                "description": "Background worker pushes events; main drains them into the spinner",
                "callback": self.example_simulated_agent,
            },
        ]
