"""Tests for DebugPromptResponse."""

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.testing.abstract_prompt_response_test import AbstractPromptResponseTest


class TestDebugPromptResponse(AbstractPromptResponseTest):
    """Test cases for DebugPromptResponse."""

    def create_test_response(self, text: str, **kwargs) -> AbstractPromptResponse:
        from wexample_prompt.responses.messages.debug_prompt_response import (
            DebugPromptResponse,
        )

        return DebugPromptResponse.create_debug(
            message=text,
            **kwargs
        )

    def _assert_specific_format(self, rendered: str):
        # Debug messages should include the debug symbol
        self.assert_contains_text(rendered, "🔍")

    def get_expected_lines(self) -> int:
        return 1  # Debug messages are single line
