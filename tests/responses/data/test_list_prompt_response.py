"""Tests for ListPromptResponse."""
from typing import Type
from unittest.mock import patch

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.example.example_class_with_context import ExampleClassWithContext
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.responses.data.list_prompt_response import ListPromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest


class TestListPromptResponse(AbstractPromptResponseTest):
    """Test cases for ListPromptResponse."""

    def setUp(self):
        """Set up test cases."""
        super().setUp()
        self.items = ["First", "Second", "Third"]
        self.test_message = "Test message"

    def get_response_class(self) -> Type[AbstractPromptResponse]:
        """Get the response class being tested."""
        return ListPromptResponse

    def get_io_method_name(self) -> str:
        """Get the name of the IO manager method for this response type."""
        return 'list'

    def _assert_specific_format(self, rendered: str):
        """Assert specific format for list responses."""
        # List should show bullet points
        self.assert_contains_text(rendered, "•")

    def get_expected_lines(self) -> int:
        """Get expected number of lines in rendered output."""
        return 1  # Just the list item for test_message

    def assert_common_response_structure(self, rendered: str):
        """Assert the common structure for list responses."""
        self.assert_contains_text(rendered, self.test_message)

    def create_test_response(self, text: str, **kwargs) -> ListPromptResponse:
        """Create a test list response.

        Args:
            text: Text to display
            **kwargs: Additional arguments

        Returns:
            ListPromptResponse: Test response
        """
        context = kwargs.pop('context', self.context)
        return ListPromptResponse.create_list(
            items=[text],
            context=context,
            **kwargs
        )

    def test_empty_list(self):
        """Test empty list response."""
        response = ListPromptResponse.create_list(
            items=[],
            context=self.context
        )
        rendered = response.render()
        self.assertEqual(rendered.strip(), "")

    def test_simple_list(self):
        """Test simple list items."""
        response = ListPromptResponse.create_list(
            items=self.items,
            context=self.context
        )
        rendered = response.render()
        for item in self.items:
            self.assert_contains_text(rendered, item)

    def test_nested_list(self):
        """Test nested list items."""
        items = [
            "Root item",
            "  • Sub item 1",
            "  • Sub item 2"
        ]
        response = ListPromptResponse.create_list(
            items=items,
            context=self.context
        )
        rendered = response.render()
        for item in items:
            self.assert_contains_text(rendered, item.strip())

    def test_custom_bullet(self):
        """Test list with custom bullet character."""
        bullet = "-"
        response = ListPromptResponse.create_list(
            items=self.items,
            bullet=bullet,
            context=self.context
        )
        rendered = response.render()
        for item in self.items:
            self.assert_contains_text(rendered, f"{bullet} {item}")

    def test_mixed_indentation(self):
        """Test list with mixed indentation levels."""
        items = [
            "Level 0",
            "  Level 1",
            "    Level 2",
            "Level 0 again"
        ]
        response = ListPromptResponse.create_list(
            items=items,
            context=self.context
        )
        rendered = response.render()
        lines = rendered.strip().split("\n")

        # Check indentation levels
        self.assertTrue(lines[0].startswith("• Level 0"))
        self.assertTrue(lines[1].startswith("  • Level 1"))
        self.assertTrue(lines[2].startswith("    • Level 2"))
        self.assertTrue(lines[3].startswith("• Level 0"))

    @patch('wexample_prompt.common.color_manager.ColorManager.supports_color')
    def test_custom_color(self, mock_supports_color):
        """Test response with custom color."""
        context = self.create_colored_test_context(mock_supports_color)
        response = self.create_test_response(
            self.test_message,
            context=context,
            color=TerminalColor.GREEN
        )
        rendered = response.render()
        self.assert_contains_text(rendered, self.test_message)
        self.assert_contains_text(rendered, "\033[32m")  

    def test_no_color(self):
        """Test response without color."""
        response = self.create_test_response(self.test_message, color=None)
        rendered = response.render()
        self.assert_contains_text(rendered, self.test_message)
        self.assertNotIn("\033[", rendered)  

    def test_io_manager(self):
        """Test IoManager integration."""
        result = self.io_manager.list(
            items=self.items,
            bullet="•"
        )
        self.assertIsInstance(result, ListPromptResponse)

    def test_prompt_context(self):
        """Test PromptContext implementation."""
        context = self.context
        class_with_context = ExampleClassWithContext(
            context=context,
            io_manager=self.io_manager
        )
        method = getattr(class_with_context, self.get_io_method_name())
        response = method(items=[self.test_message])  
        rendered = response.render()
        self.assert_contains_text(rendered, self.test_message)
