"""Tests for SuccessPromptResponse."""

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.testing.abstract_prompt_response_test import AbstractPromptResponseTest


class TestSuccessPromptResponse(AbstractPromptResponseTest):
    """Test cases for SuccessPromptResponse."""

    def create_test_response(self, text: str, **kwargs) -> AbstractPromptResponse:
        from wexample_prompt.responses.messages.success_prompt_response import (
            SuccessPromptResponse,
        )

        return SuccessPromptResponse.create_success(
            message=text,
            **kwargs
        )

    def _assert_specific_format(self, rendered: str):
        # Success messages should include the success symbol
        self.assert_contains_text(rendered, "✅")

    def get_expected_lines(self) -> int:
        return 1  # Success messages are single line
