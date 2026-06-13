"""Example usage of LeaderLinePromptResponse."""

from __future__ import annotations

import time
from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class LeaderLineExample(AbstractResponseExample):
    def example_class(self, indentation: int | None = None):
        from wexample_prompt.responses.interactive.leader_line_prompt_response import (
            LeaderLinePromptResponse,
        )

        return LeaderLinePromptResponse.create_leader_line(
            message="Direct render",
            state="success",
        )

    def example_extended(self) -> None:
        self._class_with_methods.leader_line(message="Class method demo")

    def example_failure_with_status(self) -> None:
        """Failure path with a free-form error string after the marker."""
        handle = self.io.leader_line("Connecting to broker").get_handle()
        time.sleep(0.3)
        handle.failure("connection refused")

    def example_manager(self) -> None:
        self.io.leader_line(message="IoManager demo")

    def example_ok_ko_preset(self) -> None:
        """ASCII-only preset for terminals without unicode support."""
        from wexample_prompt.responses.interactive.leader_line_prompt_response import (
            LeaderLinePromptResponse,
        )

        handle = self.io.leader_line(
            "Building project",
            markers=LeaderLinePromptResponse.MARKERS_PRESET_OK_KO,
        ).get_handle()
        time.sleep(0.3)
        handle.success()

    def example_pass_fail_preset(self) -> None:
        """Test-runner-flavored preset (PASS/FAIL)."""
        from wexample_prompt.responses.interactive.leader_line_prompt_response import (
            LeaderLinePromptResponse,
        )

        _markers = LeaderLinePromptResponse.MARKERS_PRESET_PASS_FAIL
        for name, ok in [("test_foo", True), ("test_bar", False), ("test_baz", True)]:
            handle = self.io.leader_line(
                name,
                markers=_markers,
            ).get_handle()
            time.sleep(0.1)
            if ok:
                handle.success()
            else:
                handle.failure("assertion error")

    def example_simple(self) -> None:
        """Default preset (✓/✗), straightforward success path."""
        handle = self.io.leader_line("Migrating database").get_handle()
        time.sleep(0.3)
        handle.success()

    def get_examples(self) -> list[dict[str, Any]]:
        return [
            {
                "title": "Simple",
                "description": "Default check-mark preset, simple success",
                "callback": self.example_simple,
            },
            {
                "title": "Failure with status",
                "description": "Show an error reason after the failure marker",
                "callback": self.example_failure_with_status,
            },
            {
                "title": "OK/KO preset",
                "description": "ASCII bracketed preset for legacy terminals",
                "callback": self.example_ok_ko_preset,
            },
            {
                "title": "PASS/FAIL preset",
                "description": "Test runner style",
                "callback": self.example_pass_fail_preset,
            },
        ]
