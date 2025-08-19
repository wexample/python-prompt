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

    def test_empty_properties(self):
        from wexample_prompt.responses.data.properties_prompt_response import (
            PropertiesPromptResponse,
        )
        response = PropertiesPromptResponse.create_properties(properties={})
        rendered = response.render()
        assert rendered == ""

    def test_simple_properties_rendering(self):
        response = self.create_test_response(properties={"name": "John Doe", "age": 30})
        rendered = response.render()
        self._assert_contains_text(rendered, "name")
        self._assert_contains_text(rendered, "John Doe")
        self._assert_contains_text(rendered, "age")
        self._assert_contains_text(rendered, "30")
        self._assert_specific_format(rendered)

    def test_nested_properties_rendering(self):
        nested = {
            "personal": {"name": "John Doe", "age": 30},
            "contact": {"email": "john@example.com", "phone": "123-456-7890"},
        }
        from wexample_prompt.responses.data.properties_prompt_response import (
            PropertiesPromptResponse,
        )
        response = PropertiesPromptResponse.create_properties(properties=nested, title=self._test_message)
        rendered = response.render()
        # Section headers and nested values appear
        self._assert_contains_text(rendered, "personal")
        self._assert_contains_text(rendered, "contact")
        self._assert_contains_text(rendered, "John Doe")
        self._assert_contains_text(rendered, "123-456-7890")
        self._assert_specific_format(rendered)

    def test_with_custom_title(self):
        custom_title = "User Information"
        response = self.create_test_response(title=custom_title)
        rendered = response.render()
        self._assert_contains_text(rendered, custom_title)
        self._assert_specific_format(rendered)

    def test_custom_nested_indent(self):
        nested = {"level0": {"level1": {"key": "value"}}}
        from wexample_prompt.responses.data.properties_prompt_response import (
            PropertiesPromptResponse,
        )
        response = PropertiesPromptResponse.create_properties(properties=nested, nested_indent=4)
        rendered = response.render()
        # Expect at least one line with 4-space indentation
        assert any(line.startswith("    ") for line in rendered.splitlines())
        self._assert_specific_format(rendered)
