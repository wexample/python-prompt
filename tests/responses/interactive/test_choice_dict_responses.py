"""Tests for choice prompt responses."""
import unittest
from unittest.mock import patch
from wexample_prompt.responses.interactive.choice_dict_prompt_response import ChoiceDictPromptResponse
from wexample_prompt.common.prompt_context import PromptContext


class TestChoiceDictPromptResponse(unittest.TestCase):
    """Test cases for ChoiceDictPromptResponse."""

    def setUp(self):
        """Set up test cases."""
        self.context = PromptContext(terminal_width=80)
        self.question = "Select a value:"
        self.choices = {
            "key1": "Value 1",
            "key2": "Value 2"
        }

    def test_create_with_dict(self):
        """Test creating response with dictionary choices."""
        response = ChoiceDictPromptResponse.create_choice_dict(
            question=self.question,
            choices=self.choices,
            context=self.context
        )

        rendered = response.render()
        self.assertIn(self.question, rendered)
        self.assertIn("Value 1", rendered)
        self.assertIn("Value 2", rendered)
        self.assertNotIn("key1", rendered)  # Keys should not be displayed
        self.assertNotIn("key2", rendered)

    @patch('InquirerPy.inquirer.select')
    def test_execute_returns_key(self, mock_select):
        """Test execute returns the dictionary key."""
        mock_select.return_value.execute.return_value = "key1"

        response = ChoiceDictPromptResponse.create_choice_dict(
            question=self.question,
            choices=self.choices,
            context=self.context
        )

        result = response.execute()
        self.assertEqual(result, "key1")
        mock_select.assert_called_once()
