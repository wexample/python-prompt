"""Tests for PropertiesPromptResponse."""
from typing import Type
from unittest.mock import patch

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.responses.data.properties_prompt_response import PropertiesPromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest


class TestPropertiesPromptResponse(AbstractPromptResponseTest):
    """Test cases for PropertiesPromptResponse."""

    def setUp(self):
        super().setUp()
        self.properties = {
            "name": "John Doe",
            "age": 30,
            "email": "john@example.com"
        }
        self.nested_properties = {
            "personal": {
                "name": "John Doe",
                "age": 30
            },
            "contact": {
                "email": "john@example.com",
                "phone": "123-456-7890"
            }
        }
        from wexample_prompt.example.example_class_with_context import ExampleClassWithContext
        self.class_with_context = ExampleClassWithContext(
            context=self.context,
            io=self.io
        )

    def get_response_class(self) -> Type[AbstractPromptResponse]:
        return PropertiesPromptResponse

    def get_io_method_name(self) -> str:
        return 'properties'

    def get_expected_lines(self) -> int:
        return 7  # Empty lines (2) + box borders (2) + content lines (3)

    def _assert_specific_format(self, rendered: str):
        """Assert format specific to properties response."""
        # Check box borders
        lines = rendered.split("\n")
        non_empty_lines = [line for line in lines if line.strip()]
        
        # Should have at least one border line
        self.assertTrue(any("-" in line for line in non_empty_lines))
        
        # Should have key-value pairs
        self.assertTrue(any(":" in line for line in non_empty_lines))

    def create_test_response(self, text: str, **kwargs) -> PropertiesPromptResponse:
        context = kwargs.pop('context', self.context)
        return PropertiesPromptResponse.create_properties(
            properties=self.properties,
            context=context,
            **kwargs
        )

    def test_empty_properties(self):
        response = PropertiesPromptResponse.create_properties(
            properties={},
            context=self.context
        )
        self.assertEqual(response.render(), "")

    def test_simple_properties(self):
        response = self.create_test_response(self.test_message)
        rendered = response.render()

        self.assert_contains_text(rendered, "name")
        self.assert_contains_text(rendered, "John Doe")
        self.assert_contains_text(rendered, "age")
        self.assert_contains_text(rendered, "30")
        self._assert_specific_format(rendered)

    def test_nested_properties(self):
        response = PropertiesPromptResponse.create_properties(
            properties=self.nested_properties,
            context=self.context
        )
        rendered = response.render()

        self.assert_contains_text(rendered, "personal")
        self.assert_contains_text(rendered, "contact")
        self.assert_contains_text(rendered, "John Doe")
        self.assert_contains_text(rendered, "123-456-7890")
        self._assert_specific_format(rendered)

    def test_with_title(self):
        title = "User Information"
        response = PropertiesPromptResponse.create_properties(
            properties=self.properties,
            title=title,
            context=self.context
        )
        rendered = response.render()
        self.assert_contains_text(rendered, title)
        self._assert_specific_format(rendered)

    def test_custom_indent(self):
        response = PropertiesPromptResponse.create_properties(
            properties=self.nested_properties,
            nested_indent=4,
            context=self.context
        )
        rendered = response.render()
        self.assertTrue(rendered.count(" " * 4) > 0)
        self._assert_specific_format(rendered)

    def test_io_manager(self):
        result = self.io.properties(
            properties=self.properties
        )
        self.assertIsInstance(result, PropertiesPromptResponse)
        rendered = result.render()
        self.assert_contains_text(rendered, "John Doe")
        self._assert_specific_format(rendered)

    def test_prompt_context(self):
        context = self.context
        class_with_context = self.class_with_context
        self.assertTrue(hasattr(class_with_context, 'properties'))

    @patch('wexample_prompt.common.color_manager.ColorManager.supports_color')
    def test_custom_color(self, mock_supports_color):
        context = self.create_colored_test_context(mock_supports_color)
        response = self.create_test_response(self.test_message, context=context, color=TerminalColor.GREEN)
        rendered = response.render()
        self.assert_contains_text(rendered, "John Doe")
        self._assert_specific_format(rendered)

    def test_no_color(self):
        response = self.create_test_response(self.test_message, color=None)
        rendered = response.render()
        self.assert_contains_text(rendered, "John Doe")
        self._assert_specific_format(rendered)

    def test_response_class(self):
        """Test response class behavior."""
        response = self.create_test_response(self.test_message)
        rendered = response.render()

        self.assert_common_response_structure(rendered)
        for key, value in self.properties.items():
            self.assert_contains_text(rendered, str(key))
            self.assert_contains_text(rendered, str(value))
