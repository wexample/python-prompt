"""Tests for TaskPromptResponse."""

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.testing.abstract_prompt_response_test import AbstractPromptResponseTest


class TestTaskPromptResponse(AbstractPromptResponseTest):
    """Test cases for TaskPromptResponse."""

    def create_test_response(self, **kwargs) -> AbstractPromptResponse:
        from wexample_prompt.responses.messages.task_prompt_response import (
            TaskPromptResponse,
        )

        kwargs.setdefault("message", self._test_message)
        return TaskPromptResponse.create_task(**kwargs)

    def _assert_specific_format(self, rendered: str):
        # Task messages should include the task symbol
        self._assert_contains_text(rendered, "⚡")

    def get_expected_lines(self) -> int:
        return 1  # Task messages are single line
