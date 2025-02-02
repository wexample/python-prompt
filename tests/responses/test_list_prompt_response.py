"""Tests for ListPromptResponse."""
import unittest

from wexample_prompt.responses.data.list_prompt_response import ListPromptResponse
from wexample_prompt.common.prompt_context import PromptContext


class TestListPromptResponse(unittest.TestCase):
    """Test cases for ListPromptResponse."""
    
    def setUp(self):
        """Set up test cases."""
        self.context = PromptContext(terminal_width=80)
        self.items = ["First", "Second", "Third"]
        
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
            self.assertIn(item, rendered)
            
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
            self.assertIn(item.strip(), rendered)
            
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
            self.assertIn(f"{bullet} {item}", rendered)
            
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
