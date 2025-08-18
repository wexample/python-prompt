"""Tests for InfoPromptResponse."""

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.testing.abstract_prompt_response_test import AbstractPromptResponseTest


class TestInfoPromptResponse(AbstractPromptResponseTest):
    """Test cases for InfoPromptResponse."""

    def create_test_response(self, text: str, **kwargs) -> AbstractPromptResponse:
        from wexample_prompt.responses.messages.info_prompt_response import (
            InfoPromptResponse,
        )

        return InfoPromptResponse.create_info(
            message=text,
            **kwargs
        )

    def _assert_specific_format(self, rendered: str):
        # Info messages should include the info symbol
        self.assert_contains_text(rendered, "ℹ")

    def get_expected_lines(self) -> int:
        return 1  # Info messages are single line
