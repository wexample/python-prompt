"""Tests for TablePromptResponse."""

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.testing.abstract_prompt_response_test import AbstractPromptResponseTest


class TestTablePromptResponse(AbstractPromptResponseTest):
    """Test cases for TablePromptResponse."""

    def create_test_response(self, **kwargs) -> AbstractPromptResponse:
        from wexample_prompt.responses.data.table_prompt_response import (
            TablePromptResponse,
        )

        kwargs.setdefault("headers", ["Name", "Age", "City"])
        kwargs.setdefault("data", [
            ["John", "30", "New York"],
            ["Jane", "25", "San Francisco"],
            ["Bob", "35", "Chicago"],
        ])
        kwargs.setdefault("title", self._test_message)
        return TablePromptResponse.create_table(**kwargs)

    def _assert_specific_format(self, rendered: str):
        # Should include table borders/separators
        self.assertTrue("|" in rendered or "+" in rendered)

    def get_expected_lines(self) -> int:
        # Empty lines (2) + title (1) + header (1) + 2 separators + 3 data rows
        return 9
