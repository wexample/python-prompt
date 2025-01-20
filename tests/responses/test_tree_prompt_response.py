"""Tests for TreePromptResponse."""
import unittest

from wexample_prompt.responses.tree_prompt_response import TreePromptResponse
from wexample_prompt.common.prompt_context import PromptContext


class TestTreePromptResponse(unittest.TestCase):
    """Test cases for TreePromptResponse."""
    
    def setUp(self):
        """Set up test cases."""
        self.context = PromptContext(terminal_width=80)
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
        
    def test_create_tree(self):
        """Test tree creation and rendering."""
        tree = TreePromptResponse.create_tree(
            data=self.test_data,
            context=self.context
        )
        rendered = tree.render()
        
        # Check structure
        self.assertIn("root", rendered)
        self.assertIn("folder1", rendered)
        self.assertIn("folder2", rendered)
        self.assertIn("file1", rendered)
        self.assertIn("file2", rendered)
        self.assertIn("file3", rendered)
        
        # Check default styles
        self.assertIn("├", rendered)  # branch
        self.assertIn("└", rendered)  # leaf
        self.assertIn("│", rendered)  # pipe
        self.assertIn("──", rendered)  # dash
        
    def test_empty_tree(self):
        """Test empty tree handling."""
        tree = TreePromptResponse.create_tree(
            data={},
            context=self.context
        )
        rendered = tree.render()
        self.assertEqual(rendered.strip(), "")
        
    def test_single_node(self):
        """Test tree with single node."""
        data = {"root": "value"}
        tree = TreePromptResponse.create_tree(
            data=data,
            context=self.context
        )
        rendered = tree.render()
        self.assertIn("root", rendered)
        self.assertIn("value", rendered)
        
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
        tree = TreePromptResponse.create_tree(
            data=data,
            context=self.context
        )
        rendered = tree.render()
        
        # Check all levels are present
        self.assertIn("level1", rendered)
        self.assertIn("level2", rendered)
        self.assertIn("level3", rendered)
        self.assertIn("level4", rendered)
        self.assertIn("value", rendered)
        
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
        tree = TreePromptResponse.create_tree(
            data=data,
            context=self.context
        )
        rendered = tree.render()
        
        # Check structure
        self.assertIn("root", rendered)
        self.assertIn("valid", rendered)
        self.assertIn("value", rendered)
        self.assertIn("none", rendered)
        self.assertNotIn("None", rendered)  # None values should be skipped
