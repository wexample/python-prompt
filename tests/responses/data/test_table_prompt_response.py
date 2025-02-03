"""Tests for TablePromptResponse."""
from typing import Type
from unittest.mock import patch

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.example.example_class_with_context import ExampleClassWithContext
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.responses.data.table_prompt_response import TablePromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest


class TestTablePromptResponse(AbstractPromptResponseTest):
    """Test cases for TablePromptResponse."""

    def setUp(self):
        super().setUp()
        self.headers = ["Name", "Age", "City"]
        self.data = [
            ["John", "30", "New York"],
            ["Jane", "25", "San Francisco"],
            ["Bob", "35", "Chicago"]
        ]

    def get_response_class(self) -> Type[AbstractPromptResponse]:
        return TablePromptResponse

    def get_io_method_name(self) -> str:
        return 'table'

    def get_expected_lines(self) -> int:
        """Get expected number of lines in the rendered output."""
        return 9  # Empty lines (2) + title line (1) + separator lines (2) + header line (1) + data lines (3)

    def _assert_specific_format(self, rendered: str):
        """Assert format specific to table response."""
        lines = rendered.split("\n")
        non_empty_lines = [line for line in lines if line.strip()]
        
        # Should have borders
        self.assertTrue(any("|" in line for line in non_empty_lines))
        self.assertTrue(any("+" in line for line in non_empty_lines))

    def create_test_response(self, text: str, **kwargs) -> TablePromptResponse:
        context = kwargs.pop('context', self.context)
        return TablePromptResponse.create_table(
            data=self.data,
            headers=self.headers,
            title=text,
            context=context,
            **kwargs
        )

    def test_create_table_without_headers(self):
        """Test table creation without headers."""
        response = TablePromptResponse.create_table(
            data=self.data,
            context=self.context
        )
        rendered = response.render()
        self.assert_contains_text(rendered, "John")
        self.assert_contains_text(rendered, "30")
        self.assert_contains_text(rendered, "New York")

    def test_empty_table(self):
        """Test empty table handling."""
        response = TablePromptResponse.create_table(
            data=[],
            context=self.context
        )
        rendered = response.render()
        self.assertEqual(rendered.strip(), "")

    def test_single_column(self):
        """Test single column table."""
        data = [
            ["Row 1"],
            ["Row 2"]
        ]
        headers = ["Header"]
        response = TablePromptResponse.create_table(
            data=data,
            headers=headers,
            context=self.context
        )
        rendered = response.render()
        self.assert_contains_text(rendered, "Header")
        self.assert_contains_text(rendered, "Row 1")
        self.assert_contains_text(rendered, "Row 2")

    def test_column_alignment(self):
        """Test that columns are properly aligned."""
        response = TablePromptResponse.create_table(
            data=self.data,
            headers=self.headers,
            context=self.context
        )
        rendered = response.render()
        lines = rendered.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        # All lines should start with | and end with |
        for line in non_empty_lines:
            if not line.startswith("+"):  # Skip border lines
                self.assertTrue(line.startswith("|"))
                self.assertTrue(line.endswith("|"))

    @patch('wexample_prompt.common.color_manager.ColorManager.supports_color')
    def test_custom_color(self, mock_supports_color):
        context = self.create_colored_test_context(mock_supports_color)
        response = self.create_test_response(self.test_message, context=context, color=TerminalColor.GREEN)
        rendered = response.render()
        self.assert_contains_text(rendered, self.test_message)
        self._assert_specific_format(rendered)

    def test_no_color(self):
        response = self.create_test_response(self.test_message, color=None)
        rendered = response.render()
        self.assert_contains_text(rendered, self.test_message)
        self._assert_specific_format(rendered)

    def test_io_manager(self):
        """Test IoManager integration."""
        response = self.io_manager.table(
            data=self.data,
            headers=self.headers,
            title=self.test_message
        )
        rendered = response.render()
        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.test_message)
        self._assert_specific_format(rendered)

    def test_prompt_context(self):
        """Test PromptContext implementation."""
        context = self.context
        class_with_context = ExampleClassWithContext(
            context=context,
            io_manager=self.io_manager
        )
        response = class_with_context.table(
            data=self.data,
            headers=self.headers,
            title=self.test_message
        )
        rendered = response.render()
        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.test_message)
        self._assert_specific_format(rendered)
