"""Tests for SuggestionsPromptResponse."""

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.testing.abstract_prompt_response_test import AbstractPromptResponseTest


class TestSuggestionsPromptResponse(AbstractPromptResponseTest):
    """Test cases for SuggestionsPromptResponse."""

    def create_test_response(self, text: str, **kwargs) -> AbstractPromptResponse:
        from wexample_prompt.responses.data.suggestions_prompt_response import (
            SuggestionsPromptResponse,
        )

        return SuggestionsPromptResponse.create_suggestions(
            message=text,
            suggestions=["command1 --arg value", "command2", "command3 --flag"],
            **kwargs
        )

    def _assert_specific_format(self, rendered: str):
        # Should include arrow indicators
        self._assert_contains_text(rendered, "→")

    def get_expected_lines(self) -> int:
        # Empty lines (2) + message (1) + 3 suggestions
        return 6
