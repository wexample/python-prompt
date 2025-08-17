"""Tests for TreePromptResponse."""
from typing import Type
from unittest.mock import patch

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.example.example_class_with_context import ExampleClassWithContext
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.responses.data.tree_prompt_response import TreePromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest


class TestTreePromptResponse(AbstractPromptResponseTest):
    """Test cases for TreePromptResponse."""

    def setUp(self):
        super().setUp()
        self.test_data = {
            "root": {
                "folder1": {
                    "file1": "content1",
                    "file2": "content2"
                },
                "folder2": {
                    "file3": "content3"
                }
            }
        }

    def get_response_class(self) -> Type[AbstractPromptResponse]:
        return TreePromptResponse

    def get_io_method_name(self) -> str:
        return 'tree'

    def get_expected_lines(self) -> int:
        """Get expected number of lines in the rendered output."""
        return 11  # empty lines (2) + root + folder1 (2 files with content) + folder2 (1 file with content)

    def _assert_specific_format(self, rendered: str):
        """Assert format specific to tree response."""
        # Check default styles
        self.assertIn("├", rendered)  # branch
        self.assertIn("└", rendered)  # leaf
        self.assertIn("│", rendered)  # pipe
        self.assertIn("──", rendered)  # dash

    def create_test_response(self, text: str, **kwargs) -> TreePromptResponse:
        context = kwargs.pop('context', self.context)
        return TreePromptResponse.create_tree(
            data=self.test_data,
            context=context,
            **kwargs
        )

    def test_empty_tree(self):
        """Test empty tree handling."""
        response = TreePromptResponse.create_tree(
            data={},
            context=self.context
        )
        rendered = response.render()
        self.assertEqual(rendered.strip(), "")

    def test_single_node(self):
        """Test tree with single node."""
        data = {"root": "value"}
        response = TreePromptResponse.create_tree(
            data=data,
            context=self.context
        )
        rendered = response.render()
        self.assert_contains_text(rendered, "root")
        self.assert_contains_text(rendered, "value")

    def test_deep_nesting(self):
        """Test deeply nested tree structure."""
        data = {
            "level1": {
                "level2": {
                    "level3": {
                        "level4": "value"
                    }
                }
            }
        }
        response = TreePromptResponse.create_tree(
            data=data,
            context=self.context
        )
        rendered = response.render()

        # Check all levels are present
        self.assert_contains_text(rendered, "level1")
        self.assert_contains_text(rendered, "level2")
        self.assert_contains_text(rendered, "level3")
        self.assert_contains_text(rendered, "level4")
        self.assert_contains_text(rendered, "value")

        # Check indentation increases
        lines = rendered.split('\n')
        indents = [len(line) - len(line.lstrip()) for line in lines if line.strip()]
        self.assertEqual(sorted(indents), indents, "Indentation should increase with depth")

    def test_none_values(self):
        """Test tree with None values."""
        data = {
            "root": {
                "valid": "value",
                "none": None
            }
        }
        response = TreePromptResponse.create_tree(
            data=data,
            context=self.context
        )
        rendered = response.render()

        # Check structure
        self.assert_contains_text(rendered, "root")
        self.assert_contains_text(rendered, "valid")
        self.assert_contains_text(rendered, "value")
        self.assert_contains_text(rendered, "none")
        self.assertNotIn("None", rendered)  # None values should be skipped

    @patch('wexample_prompt.common.color_manager.ColorManager.supports_color')
    def test_custom_color(self, mock_supports_color):
        context = self.create_colored_test_context(mock_supports_color)
        response = self.create_test_response(self.test_message, context=context, color=TerminalColor.GREEN)
        rendered = response.render()
        self.assert_contains_text(rendered, "root")
        self._assert_specific_format(rendered)

    def test_no_color(self):
        response = self.create_test_response(self.test_message, color=None)
        rendered = response.render()
        self.assert_contains_text(rendered, "root")
        self._assert_specific_format(rendered)

    def test_io_manager(self):
        """Test IoManager integration."""
        response = self.io.tree(data=self.test_data)
        rendered = response.render()
        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, "root")
        self._assert_specific_format(rendered)

    def test_prompt_context(self):
        """Test PromptContext implementation."""
        context = self.context
        class_with_context = ExampleClassWithContext(
            context=context,
            io=self.io
        )
        response = class_with_context.tree(data=self.test_data)
        rendered = response.render()
        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, "root")
        self._assert_specific_format(rendered)

    def test_response_class(self):
        """Test response class behavior."""
        response = self.create_test_response(self.test_message)
        rendered = response.render()

        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, "root")
        self._assert_specific_format(rendered)
