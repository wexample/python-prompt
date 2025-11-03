"""Example usage of ProgressPromptResponse."""

from __future__ import annotations

import time
from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


def step1() -> None:
    """First step: Initialize system."""
    time.sleep(0.2)


def step2() -> None:
    """Second step: Process data."""
    time.sleep(0.4)


def step3() -> None:
    """Third step: Cleanup."""
    time.sleep(0.2)


@base_class
class ProgressExample(AbstractResponseExample):
    """Example usage of progress responses."""

    def example_class(self, indentation: int | None = None):
        """Example using the response class directly."""
        from wexample_prompt.responses.interactive.progress_prompt_response import (
            ProgressPromptResponse,
        )

        return ProgressPromptResponse.create_progress(
            total=5,
            current=3,
            label="Processing",
        )

    def example_extended(self) -> None:
        """Example using a context class."""
        self._class_with_methods.progress(
            total=5,
            current=3,
            label="Processing",
        )

    def example_manager(self) -> None:
        """Example using the IoManager."""
        self.io.progress(
            total=5,
            current=3,
            label="Processing",
        )

    def edge_case_limits(self) -> None:
        """Test edge cases: limits (long labels)."""
        # Very long label
        response = self.io.progress(
            label='@color:cyan{This is a very long progress label that contains lots of text and should test wrapping behavior}',
            total=100
        )
        handle = response.get_handle()
        for cur in (25, 50, 75, 100):
            time.sleep(0.02)
            handle.update(current=cur)

    def edge_case_indentation(self) -> None:
        """Test edge cases: indentation."""
        response = self.io.progress(
            label='@color:cyan{Level 0}',
            total=100,
            indentation=0
        )
        handle = response.get_handle()
        handle.update(current=50)
        handle.finish()

        self.io.indentation = 3
        response = self.io.progress(
            label='@color:yellow{Level 3 indentation}',
            total=100
        )
        handle = response.get_handle()
        handle.update(current=50)
        handle.finish()

        response = self.io.progress(
            label='@color:magenta{Level 3 + 5 indentation}',
            total=100,
            indentation=5
        )
        handle = response.get_handle()
        handle.update(current=50)
        handle.finish()
        self.io.indentation = 0

    def edge_case_nesting(self) -> None:
        """Test edge cases: nested progress bars."""
        response = self.io.progress(label='@color:cyan+bold{Main Task}', total=3)
        root = response.get_handle()

        stages = ['Compilation', 'Testing', 'Packaging']

        for stage_idx, stage_name in enumerate(stages):
            self.io.indentation += 1
            stage_handle = root.create_range_handle(
                to_step=1,
                virtual_total=5
            )

            for step in range(1, 6):
                time.sleep(0.01)
                stage_handle.advance(
                    step=1,
                    label=f"@color:yellow{{{stage_name}: step {step}/5}}"
                )

            stage_handle.finish(label=f"@color:green+bold{{{stage_name} complete}}")
            self.io.indentation -= 1

        root.finish(label="@🟢+bold{Build complete}")

    def get_examples(self) -> list[dict[str, Any]]:
        """Get list of examples.

        Returns:
            List of example configurations
        """
        return [
            {
                "title": "Basic Progress",
                "description": "Simple progress bar",
                "callback": self.example_manager,
            },
            {
                "title": "Edge Case: Limits",
                "description": "Long labels in progress bars",
                "callback": self.edge_case_limits,
            },
            {
                "title": "Edge Case: Indentation",
                "description": "Progress with various indentation levels",
                "callback": self.edge_case_indentation,
            },
            {
                "title": "Edge Case: Nesting",
                "description": "Nested progress bars",
                "callback": self.edge_case_nesting,
            },
        ]
