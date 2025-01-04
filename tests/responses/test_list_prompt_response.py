"""Tests for ListPromptResponse."""
import unittest

from wexample_prompt.responses.list_prompt_response import ListPromptResponse
from wexample_prompt.common.prompt_context import PromptContext


class TestListPromptResponse(unittest.TestCase):
    """Test cases for ListPromptResponse."""
    
    def setUp(self):
        """Set up test cases."""
        self.context = PromptContext(terminal_width=80)
        
    def test_empty_list(self):
        """Test empty list response."""
        response = ListPromptResponse.create([])
        rendered = response.render()
        self.assertEqual(rendered.strip(), "")
        
    def test_simple_list(self):
        """Test simple list items."""
        items = ["First", "Second", "Third"]
        response = ListPromptResponse.create(items)
        rendered = response.render()
        for item in items:
            self.assertIn(item, rendered)
            
    def test_nested_list(self):
        """Test nested list items."""
        items = [
            "Root item",
            "  • Sub item 1",
            "  • Sub item 2"
        ]
        response = ListPromptResponse.create(items)
        rendered = response.render()
        for item in items:
            self.assertIn(item.strip(), rendered)
