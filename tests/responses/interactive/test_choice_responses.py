"""Tests for choice prompt responses."""
from typing import Type
from unittest.mock import patch

from InquirerPy.base.control import Choice

from wexample_prompt.example.example_class_with_context import ExampleClassWithContext
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.responses.interactive.choice_prompt_response import ChoicePromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest


class TestChoicePromptResponse(AbstractPromptResponseTest):
    """Test cases for ChoicePromptResponse."""

    def setUp(self):
        """Set up test cases."""
        super().setUp()
        self.question = "Select an option:"
        self.choices = ["Option 1", "Option 2"]

    def get_response_class(self) -> Type[AbstractPromptResponse]:
        return ChoicePromptResponse

    def create_test_response(self, text: str, **kwargs) -> AbstractPromptResponse:
        context = kwargs.pop('context', self.context)
        return ChoicePromptResponse.create_choice(
            question=text,
            choices=self.choices,
            context=context,
            **kwargs
        )

    def get_io_method_name(self) -> str:
        return 'choice'

    def _assert_specific_format(self, rendered: str):
        # Choice prompts should have arrow indicators and numbering
        self.assert_contains_text(rendered, "→")
        self.assert_contains_text(rendered, "1.")
        self.assert_contains_text(rendered, "2.")

    def get_expected_lines(self) -> int:
        return len(self.choices) + 2  # Question + choices + abort

    def assert_common_response_structure(self, rendered: str):
        """Assert the common structure for choice responses.
        
        Overrides the parent method since choice responses have a different structure.
        """
        lines = rendered.split('\n')
        
        # First line should contain the question
        self.assert_contains_text(lines[0], self.test_message)
        
        # Should have the correct number of lines
        self.assertEqual(len([l for l in lines if l.strip()]), self.get_expected_lines())
        
        # Each choice line should be properly formatted
        for i, choice in enumerate(self.choices, start=1):
            choice_line = lines[i]
            self.assert_contains_text(choice_line, f"{i}.")
            self.assert_contains_text(choice_line, "→")
            self.assert_contains_text(choice_line, choice)

    def test_create_with_choice_objects(self):
        """Test creating response with Choice objects."""
        choices = [
            Choice("value1", "Display 1"),
            Choice("value2", "Display 2")
        ]
        response = ChoicePromptResponse.create_choice(
            question=self.test_message,
            choices=choices,
            context=self.context
        )

        rendered = response.render()
        self.assert_contains_text(rendered, "Display 1")
        self.assert_contains_text(rendered, "Display 2")
        self.assertNotIn("value1", rendered)  # Values should not be displayed
        self.assertNotIn("value2", rendered)

    def test_abort_option(self):
        """Test abort option is included when specified."""
        abort_text = "Cancel"
        response = self.create_test_response(
            self.test_message,
            abort=abort_text
        )

        rendered = response.render()
        self.assert_contains_text(rendered, abort_text)
        self.assert_contains_text(rendered, str(len(self.choices) + 1))  # Check abort numbering

    @patch('InquirerPy.inquirer.select')
    def test_execute_returns_selection(self, mock_select):
        """Test execute returns the selected value."""
        expected_value = "Option 1"
        mock_select.return_value.execute.return_value = expected_value

        response = self.create_test_response(self.test_message)

        result = response.execute()
        self.assertEqual(result, expected_value)
        mock_select.assert_called_once()

    def test_no_abort_option(self):
        """Test response without abort option."""
        response = self.create_test_response(
            self.test_message,
            abort=None
        )

        rendered = response.render()
        self.assertNotIn("> Abort", rendered)
        self.assertEqual(
            len([line for line in rendered.split('\n') if line.strip()]),
            len(self.choices) + 1  # choices + question
        )

    @patch('InquirerPy.inquirer.select')
    def test_io_manager(self, mock_select):
        """Test IoManager integration."""
        expected_value = "Option 1"
        mock_select.return_value.execute.return_value = expected_value

        method = getattr(self.io_manager, self.get_io_method_name())
        result = method(self.test_message, self.choices)

        # Verify the result
        self.assertEqual(result, expected_value)
        mock_select.assert_called_once()

    @patch('InquirerPy.inquirer.select')
    def test_prompt_context(self, mock_select):
        """Test PromptContext implementation."""
        expected_value = "Option 1"
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
