"""Tests for choice prompt responses."""
import unittest
from io import StringIO
from unittest.mock import patch

from InquirerPy.base.control import Choice

from wexample_prompt.responses import ChoicePromptResponse, ChoiceDictPromptResponse
from wexample_prompt.common.prompt_context import PromptContext


class TestChoicePromptResponse(unittest.TestCase):
    """Test cases for ChoicePromptResponse."""

    def setUp(self):
        """Set up test cases."""
        self.output = StringIO()
        self.context = PromptContext(color_enabled=True)

    def test_create_simple_choices(self):
        """Test creating response with simple choices."""
        response = ChoicePromptResponse.create(
            question="Select an option:",
            choices=["Option 1", "Option 2"],
            context=self.context
        )
        
        # Check question and choices are present
        rendered = response.render()
        self.assertIn("Select an option:", rendered)
        self.assertIn("Option 1", rendered)
        self.assertIn("Option 2", rendered)
        
        # Check formatting
        self.assertIn("→", rendered)  # Arrow indicator

    def test_create_with_choice_objects(self):
        """Test creating response with Choice objects."""
        choices = [
            Choice("value1", "Display 1"),
            Choice("value2", "Display 2")
        ]
        response = ChoicePromptResponse.create(
            question="Select:",
            choices=choices,
            context=self.context
        )
        
        rendered = response.render()
        self.assertIn("Display 1", rendered)
        self.assertIn("Display 2", rendered)

    def test_abort_option(self):
        """Test abort option is included when specified."""
        response = ChoicePromptResponse.create(
            question="Select:",
            choices=["Option"],
            abort="Cancel",
            context=self.context
        )
        
        rendered = response.render()
        self.assertIn("Cancel", rendered)

    @patch('InquirerPy.inquirer.select')
    def test_execute_returns_selection(self, mock_select):
        """Test execute returns the selected value."""
        mock_select.return_value.execute.return_value = "Option 1"
        
        response = ChoicePromptResponse.create(
            question="Select:",
            choices=["Option 1", "Option 2"]
        )
        
        result = response.execute()
        self.assertEqual(result, "Option 1")


class TestChoiceDictPromptResponse(unittest.TestCase):
    """Test cases for ChoiceDictPromptResponse."""

    def setUp(self):
        """Set up test cases."""
        self.output = StringIO()
        self.context = PromptContext(color_enabled=True)
        self.choices = {
            "key1": "Value 1",
            "key2": "Value 2"
        }

    def test_create_with_dict(self):
        """Test creating response with dictionary choices."""
        response = ChoiceDictPromptResponse.create(
            question="Select:",
            choices=self.choices,
            context=self.context
        )
        
        rendered = response.render()
        self.assertIn("Value 1", rendered)
        self.assertIn("Value 2", rendered)
        # Keys should not be visible in the output
        self.assertNotIn("key1", rendered)
        self.assertNotIn("key2", rendered)

    def test_default_value(self):
        """Test default value is properly handled."""
        response = ChoiceDictPromptResponse.create(
            question="Select:",
            choices=self.choices,
            default="key1"
        )
        
        # Default value should be converted to display text
        self.assertEqual(response._default, "Value 1")

    @patch('InquirerPy.inquirer.select')
    def test_execute_returns_key(self, mock_select):
        """Test execute returns the key of selected value."""
        mock_select.return_value.execute.return_value = "Value 1"
        
        response = ChoiceDictPromptResponse.create(
            question="Select:",
            choices=self.choices
        )
        
        result = response.execute()
        self.assertEqual(result, "key1")

    @patch('InquirerPy.inquirer.select')
    def test_execute_returns_none_on_abort(self, mock_select):
        """Test execute returns None when aborted."""
        mock_select.return_value.execute.return_value = None
        
        response = ChoiceDictPromptResponse.create(
            question="Select:",
            choices=self.choices,
            abort="Cancel"
        )
        
        result = response.execute()
        self.assertIsNone(result)
