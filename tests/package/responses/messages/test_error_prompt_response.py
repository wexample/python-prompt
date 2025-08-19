"""Tests for ErrorPromptResponse."""

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.testing.abstract_prompt_response_test import AbstractPromptResponseTest


class TestErrorPromptResponse(AbstractPromptResponseTest):
    """Test cases for ErrorPromptResponse."""

    def create_test_response(self, **kwargs) -> AbstractPromptResponse:
        from wexample_prompt.responses.messages.error_prompt_response import (
            ErrorPromptResponse,
        )

        kwargs.setdefault("message", self._test_message)
        return ErrorPromptResponse.create_error(**kwargs)

    def _assert_specific_format(self, rendered: str):
        # Error messages should include the error symbol
        self._assert_contains_text(rendered, "❌")

    def get_expected_lines(self) -> int:
        return 1  # Error messages are single line
