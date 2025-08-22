"""Tests for TaskPromptResponse."""
from __future__ import annotations

from wexample_helpers.const.types import Kwargs
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.testing.abstract_prompt_message_response_test import (
    AbstractPromptMessageResponseTest,
)


class TestTaskPromptResponse(AbstractPromptMessageResponseTest):
    """Test cases for TaskPromptResponse."""

    def _get_response_class(self) -> type[AbstractPromptResponse]:
        from wexample_prompt.responses.messages.task_prompt_response import (
            TaskPromptResponse,
        )

        return TaskPromptResponse

    def _create_test_kwargs(self, kwargs=None) -> Kwargs:
        kwargs = kwargs or {}
        kwargs.setdefault("message", self._test_message)
        return kwargs

    def _assert_specific_format(self, rendered: str) -> None:
        # Task messages should include the task symbol
        self._assert_contains_text(rendered, "⚡")

    def get_expected_lines(self) -> int:
        return 1  # Task messages are single line
