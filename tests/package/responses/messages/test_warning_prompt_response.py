"""Tests for WarningPromptResponse."""

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.testing.abstract_prompt_message_response_test import AbstractPromptMessageResponseTest


class TestWarningPromptResponse(AbstractPromptMessageResponseTest):
    """Test cases for WarningPromptResponse."""

    def create_test_response(self, **kwargs) -> AbstractPromptResponse:
        from wexample_prompt.responses.messages.warning_prompt_response import (
            WarningPromptResponse,
        )

        kwargs.setdefault("message", self._test_message)
        return WarningPromptResponse.create_warning(**kwargs)

    def _assert_specific_format(self, rendered: str):
        # Warning messages should include the warning symbol
        self._assert_contains_text(rendered, "⚠")

    def get_expected_lines(self) -> int:
        return 1  # Warning messages are single line
