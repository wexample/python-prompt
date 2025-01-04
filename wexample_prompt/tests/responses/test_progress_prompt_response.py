"""Tests for ProgressPromptResponse."""
import unittest

from wexample_prompt.responses.progress_prompt_response import ProgressPromptResponse
from wexample_prompt.common.prompt_context import PromptContext


class TestProgressPromptResponse(unittest.TestCase):
    """Test cases for ProgressPromptResponse."""
    
    def setUp(self):
        """Set up test cases."""
        self.context = PromptContext(terminal_width=80)
        
    def test_create_progress(self):
        """Test progress bar creation."""
        progress = ProgressPromptResponse.create(total=100, current=50)
        rendered = progress.render()
        
        # Check basic structure
        self.assertIn("[", rendered)  # Start bracket
        self.assertIn("]", rendered)  # End bracket
        self.assertIn("=", rendered)  # Progress indicator
        self.assertIn("50%", rendered)  # Percentage
        
    def test_zero_progress(self):
        """Test progress bar at 0%."""
        progress = ProgressPromptResponse.create(total=100, current=0)
        rendered = progress.render()
        self.assertIn("[" + " " * 50 + "]", rendered)  # Should be empty
        self.assertIn("0%", rendered)
        
    def test_full_progress(self):
        """Test progress bar at 100%."""
        progress = ProgressPromptResponse.create(total=100, current=100)
        rendered = progress.render()
        self.assertIn("[" + "=" * 50 + "]", rendered)  # Should be full
        self.assertIn("100%", rendered)
        
    def test_partial_progress(self):
        """Test progress bar with partial completion."""
        progress = ProgressPromptResponse.create(total=10, current=7)
        rendered = progress.render()
        self.assertIn("70%", rendered)
        
    def test_custom_width(self):
        """Test progress bar with custom width."""
        width = 20
        progress = ProgressPromptResponse.create(total=100, current=50, width=width)
        rendered = progress.render()
        expected_filled = "=" * (width // 2)  # Half filled for 50%
        expected_empty = " " * (width - (width // 2))
        self.assertIn(f"[{expected_filled}{expected_empty}]", rendered)
        
    def test_invalid_progress(self):
        """Test handling of invalid progress values."""
        # Test zero total
        with self.assertRaises(ValueError):
            ProgressPromptResponse.create(total=0, current=10)
            
        # Test negative total
        with self.assertRaises(ValueError):
            ProgressPromptResponse.create(total=-100, current=50)
            
        # Test negative current
        with self.assertRaises(ValueError):
            ProgressPromptResponse.create(total=100, current=-10)
            
        # Test invalid width
        with self.assertRaises(ValueError):
            ProgressPromptResponse.create(total=100, current=50, width=0)
            
        # Test current > total (should cap at 100%)
        progress = ProgressPromptResponse.create(total=100, current=150)
        rendered = progress.render()
        self.assertIn("100%", rendered)
        self.assertEqual(progress.metadata["current"], 100)  # Should be capped
        
    def test_metadata(self):
        """Test progress bar metadata."""
        total, current, width = 100, 75, 30
        progress = ProgressPromptResponse.create(total=total, current=current, width=width)
        self.assertEqual(progress.metadata["total"], total)
        self.assertEqual(progress.metadata["current"], current)
        self.assertEqual(progress.metadata["width"], width)
