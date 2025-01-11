"""Tests for choice prompt responses."""
import unittest
from unittest.mock import patch

from InquirerPy.base.control import Choice
from wexample_prompt.responses.interactive.choice_prompt_response import ChoicePromptResponse
from wexample_prompt.common.prompt_context import PromptContext


class TestChoicePromptResponse(unittest.TestCase):
    """Test cases for ChoicePromptResponse."""

    def setUp(self):
        """Set up test cases."""
        self.context = PromptContext(terminal_width=80)
        self.question = "Select an option:"
        self.choices = ["Option 1", "Option 2"]

    def test_create_simple_choices(self):
        """Test creating response with simple choices."""
        response = ChoicePromptResponse.create_choice(
            question=self.question,
            choices=self.choices,
            context=self.context
        )

        # Check question and choices are present
        rendered = response.render()
        self.assertIn(self.question, rendered)
        self.assertIn("Option 1", rendered)
        self.assertIn("Option 2", rendered)

        # Check formatting
        self.assertIn("→", rendered)  # Arrow indicator
        self.assertIn("1.", rendered)  # Numbering
        self.assertIn("2.", rendered)

    def test_create_with_choice_objects(self):
        """Test creating response with Choice objects."""
        choices = [
            Choice("value1", "Display 1"),
            Choice("value2", "Display 2")
        ]
        response = ChoicePromptResponse.create_choice(
            question=self.question,
            choices=choices,
            context=self.context
        )

        rendered = response.render()
        self.assertIn("Display 1", rendered)
        self.assertIn("Display 2", rendered)
        self.assertNotIn("value1", rendered)  # Values should not be displayed
        self.assertNotIn("value2", rendered)

    def test_abort_option(self):
        """Test abort option is included when specified."""
        abort_text = "Cancel"
        response = ChoicePromptResponse.create_choice(
            question=self.question,
            choices=self.choices,
            abort=abort_text,
            context=self.context
        )

        rendered = response.render()
        self.assertIn(abort_text, rendered)
        self.assertIn(str(len(self.choices) + 1), rendered)  # Check abort numbering

    @patch('InquirerPy.inquirer.select')
    def test_execute_returns_selection(self, mock_select):
        """Test execute returns the selected value."""
        expected_value = "Option 1"
        mock_select.return_value.execute.return_value = expected_value

        response = ChoicePromptResponse.create_choice(
            question=self.question,
            choices=self.choices,
            context=self.context
        )

        result = response.execute()
        self.assertEqual(result, expected_value)
        mock_select.assert_called_once()

    def test_no_abort_option(self):
        """Test response without abort option."""
        response = ChoicePromptResponse.create_choice(
            question=self.question,
            choices=self.choices,
            abort=None,
            context=self.context
        )

        rendered = response.render()
        self.assertNotIn("> Abort", rendered)
        self.assertEqual(
            len([line for line in rendered.split('\n') if line.strip()]),
            len(self.choices) + 1  # choices + question
        )
