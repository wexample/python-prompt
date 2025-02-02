"""Tests for choice prompt responses."""
from typing import Type
from unittest.mock import patch

from wexample_prompt.example.example_class_with_context import ExampleClassWithContext
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.responses.interactive.choice_dict_prompt_response import ChoiceDictPromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest


class TestChoiceDictPromptResponse(AbstractPromptResponseTest):
    """Test cases for ChoiceDictPromptResponse."""

    def setUp(self):
        """Set up test cases."""
        super().setUp()
        self.question = "Select a value:"
        self.choices = {
            "key1": "Value 1",
            "key2": "Value 2"
        }

    def get_response_class(self) -> Type[AbstractPromptResponse]:
        return ChoiceDictPromptResponse

    def create_test_response(self, text: str, **kwargs) -> AbstractPromptResponse:
        context = kwargs.pop('context', self.context)
        return ChoiceDictPromptResponse.create_choice_dict(
            question=text,
            choices=self.choices,
            context=context,
            **kwargs
        )

    def get_io_method_name(self) -> str:
        return 'choice_dict'

    def _assert_specific_format(self, rendered: str):
        # Choice dict prompts should have arrow indicators and numbering
        self.assert_contains_text(rendered, "→")
        self.assert_contains_text(rendered, "1.")
        self.assert_contains_text(rendered, "2.")

    def get_expected_lines(self) -> int:
        return len(self.choices) + 2  # Question + choices + abort

    def assert_common_response_structure(self, rendered: str):
        """Assert the common structure for choice dict responses.
        
        Overrides the parent method since choice dict responses have a different structure.
        """
        lines = rendered.split('\n')
        
        # First line should contain the question
        self.assert_contains_text(lines[0], self.test_message)
        
        # Should have the correct number of lines
        self.assertEqual(len([l for l in lines if l.strip()]), self.get_expected_lines())
        
        # Each choice line should be properly formatted
        for i, (key, value) in enumerate(self.choices.items(), start=1):
            choice_line = lines[i]
            self.assert_contains_text(choice_line, f"{i}.")
            self.assert_contains_text(choice_line, "→")
            self.assert_contains_text(choice_line, value)
            self.assertNotIn(key, choice_line)  # Key should not be visible

    def test_create_with_dict(self):
        """Test creating response with dictionary choices."""
        response = self.create_test_response(self.test_message)

        rendered = response.render()
        self.assert_contains_text(rendered, "Value 1")
        self.assert_contains_text(rendered, "Value 2")
        self.assertNotIn("key1", rendered)  # Keys should not be displayed
        self.assertNotIn("key2", rendered)

    @patch('InquirerPy.inquirer.select')
    def test_execute_returns_key(self, mock_select):
        """Test execute returns the dictionary key."""
        mock_select.return_value.execute.return_value = "key1"

        response = self.create_test_response(self.test_message)

        result = response.execute()
        self.assertEqual(result, "key1")
        mock_select.assert_called_once()

    @patch('InquirerPy.inquirer.select')
    def test_io_manager(self, mock_select):
        """Test IoManager integration."""
        expected_value = "key1"
        mock_select.return_value.execute.return_value = expected_value

        method = getattr(self.io_manager, self.get_io_method_name())
        result = method(self.test_message, self.choices)

        # Verify the result
        self.assertEqual(result, expected_value)
        mock_select.assert_called_once()

    @patch('InquirerPy.inquirer.select')
    def test_prompt_context(self, mock_select):
        """Test PromptContext implementation."""
        expected_value = "key1"
        mock_select.return_value.execute.return_value = expected_value

        context = self.context
        class_with_context = ExampleClassWithContext(
            context=context,
            io_manager=self.io_manager
        )
        method = getattr(class_with_context, self.get_io_method_name())
        result = method(self.test_message, self.choices)

        # Verify the result
        self.assertEqual(result, expected_value)
        mock_select.assert_called_once()
