"""Tests for ListPromptResponse."""

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.testing.abstract_prompt_response_test import AbstractPromptResponseTest


class TestListPromptResponse(AbstractPromptResponseTest):
    """Test cases for ListPromptResponse."""

    def create_test_response(self, text: str, **kwargs) -> AbstractPromptResponse:
        from wexample_prompt.responses.data.list_prompt_response import (
            ListPromptResponse,
        )

        return ListPromptResponse.create_list(
            items=[text],
            **kwargs
        )

    def _assert_specific_format(self, rendered: str):
        # List should show bullet points
        self._assert_contains_text(rendered, "•")

    def get_expected_lines(self) -> int:
        return 1  # Single list item
