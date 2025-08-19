"""Tests for FailurePromptResponse."""

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.testing.abstract_prompt_response_test import AbstractPromptResponseTest


class TestFailurePromptResponse(AbstractPromptResponseTest):
    """Test cases for FailurePromptResponse."""

    def create_test_response(self, text: str, **kwargs) -> AbstractPromptResponse:
        from wexample_prompt.responses.messages.failure_prompt_response import (
            FailurePromptResponse,
        )

        return FailurePromptResponse.create_failure(
            message=text,
            **kwargs
        )

    def _assert_specific_format(self, rendered: str):
        # Failure messages should include the failure symbol
        self._assert_contains_text(rendered, "❌")

    def get_expected_lines(self) -> int:
        return 1  # Failure messages are single line
