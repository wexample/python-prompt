"""Tests for PropertiesPromptResponse."""
import unittest

from wexample_prompt.responses.data.properties_prompt_response import PropertiesPromptResponse
from wexample_prompt.common.prompt_context import PromptContext


class TestPropertiesPromptResponse(unittest.TestCase):
    """Test cases for PropertiesPromptResponse."""

    def setUp(self):
        """Set up test cases."""
        self.context = PromptContext(terminal_width=80)
        self.simple_properties = {
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

    def test_create_simple_properties(self):
        """Test creating properties response with simple key-value pairs."""
        response = PropertiesPromptResponse.create_properties(
            properties=self.simple_properties,
            context=self.context
        )
        rendered = response.render()

        # Check basic structure
        self.assertIn("name", rendered)
        self.assertIn("John Doe", rendered)
        self.assertIn("age", rendered)
        self.assertIn("30", rendered)
        self.assertIn("email", rendered)
        self.assertIn("john@example.com", rendered)

        # Check borders
        self.assertIn("-", rendered)  # Horizontal borders

    def test_create_with_title(self):
        """Test properties response with a title."""
        title = "User Information"
        response = PropertiesPromptResponse.create_properties(
            properties=self.simple_properties,
            title=title,
            context=self.context
        )
        rendered = response.render()

        # Check title presence and format
        self.assertIn(title, rendered)
        # Title should be centered
        first_line = rendered.split("\n")[0]
        title_start = first_line.find(title)
        self.assertTrue(title_start > 0)  # Title should not start at beginning
        self.assertTrue(title_start < len(first_line) - len(title))  # Title should not end at end

    def test_nested_properties(self):
        """Test properties response with nested dictionaries."""
        response = PropertiesPromptResponse.create_properties(
            properties=self.nested_properties,
            context=self.context
        )
        rendered = response.render()

        # Check structure and indentation
        self.assertIn("personal:", rendered)
        self.assertIn("  name", rendered)  # Indented
        self.assertIn("contact:", rendered)
        self.assertIn("  email", rendered)  # Indented

    def test_custom_indent(self):
        """Test properties response with custom indentation."""
        custom_indent = 4
        response = PropertiesPromptResponse.create_properties(
            properties=self.nested_properties,
            nested_indent=custom_indent,
            context=self.context
        )
        rendered = response.render()

        # Check custom indentation
        self.assertIn("    name", rendered)  # 4 spaces
        self.assertIn("    email", rendered)  # 4 spaces

    def test_empty_properties(self):
        """Test properties response with empty dictionary."""
        response = PropertiesPromptResponse.create_properties(
            properties={},
            context=self.context
        )
        rendered = response.render()
        self.assertEqual(rendered, "")

    def test_special_characters(self):
        """Test properties response with special characters."""
        special_props = {
            "symbols": "!@#$%^&*()",
            "unicode": "Hello 世界",
            "spaces": "   padded   "
        }
        response = PropertiesPromptResponse.create_properties(
            properties=special_props,
            context=self.context
        )
        rendered = response.render()

        # Check special characters are preserved
        self.assertIn("!@#$%^&*()", rendered)
        self.assertIn("Hello 世界", rendered)
        self.assertIn("   padded   ", rendered)
