"""Tests for PropertiesPromptResponse."""

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.testing.abstract_prompt_response_test import AbstractPromptResponseTest


class TestPropertiesPromptResponse(AbstractPromptResponseTest):
    """Test cases for PropertiesPromptResponse."""

    def create_test_response(self, **kwargs) -> AbstractPromptResponse:
        from wexample_prompt.responses.data.properties_prompt_response import (
            PropertiesPromptResponse,
        )

        kwargs.setdefault("properties", {"name": "John Doe", "age": 30})
        kwargs.setdefault("title", self._test_message)
        return PropertiesPromptResponse.create_properties(**kwargs)

    def _assert_specific_format(self, rendered: str):
        # Should contain key-value formatting
        self.assertIn(":", rendered)

    def get_expected_lines(self) -> int:
        # Boxed properties typically render with top/bottom borders and content
        return 5
