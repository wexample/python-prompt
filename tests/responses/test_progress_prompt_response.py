"""Tests for ProgressPromptResponse."""
import unittest
import re

from wexample_prompt.responses.progress_prompt_response import ProgressPromptResponse
from wexample_prompt.common.prompt_context import PromptContext


class TestProgressPromptResponse(unittest.TestCase):
    """Test cases for ProgressPromptResponse."""
    
    def setUp(self):
        """Set up test cases."""
        self.context = PromptContext(terminal_width=80)
        # Use simple characters for testing
        ProgressPromptResponse.set_style(fill_char="=", empty_char="-")
        
    def test_create_progress(self):
        """Test progress bar creation."""
        progress = ProgressPromptResponse.create(total=100, current=50)
        rendered = self._strip_ansi(progress.render())
        
        # Check basic structure
        self.assertIn("=", rendered)  # Progress indicator
        self.assertIn("-", rendered)  # Empty indicator
        self.assertIn("50%", rendered)  # Percentage
        
    def test_zero_progress(self):
        """Test progress bar at 0%."""
        progress = ProgressPromptResponse.create(total=100, current=0)
        rendered = self._strip_ansi(progress.render())
        self.assertTrue(rendered.startswith("-" * 50))  # Should be empty
        self.assertIn("0%", rendered)
        
    def test_full_progress(self):
        """Test progress bar at 100%."""
        progress = ProgressPromptResponse.create(total=100, current=100)
        rendered = self._strip_ansi(progress.render())
        self.assertTrue("=" * 50 in rendered)  # Should be full
        self.assertIn("100%", rendered)
        
    def test_partial_progress(self):
        """Test progress bar with partial completion."""
        progress = ProgressPromptResponse.create(total=10, current=7)
        rendered = self._strip_ansi(progress.render())
        self.assertIn("70%", rendered)
        
    def test_custom_width(self):
        """Test progress bar with custom width."""
        width = 20
        progress = ProgressPromptResponse.create(total=100, current=50, width=width)
        rendered = self._strip_ansi(progress.render())
        expected_filled = "=" * (width // 2)  # Half filled for 50%
        expected_empty = "-" * (width - (width // 2))
        self.assertTrue(expected_filled in rendered and expected_empty in rendered)
        
    def test_label(self):
        """Test progress bar with label."""
        label = "Processing"
        progress = ProgressPromptResponse.create(
            total=100,
            current=50,
            label=label
        )
        rendered = self._strip_ansi(progress.render())
        self.assertTrue(rendered.startswith(label))  # Label should be at start
        self.assertIn("50%", rendered)  # Percentage should be present
        
    def test_invalid_progress(self):
        """Test handling of invalid progress values."""
        # Test zero total
        with self.assertRaises(ValueError):
            ProgressPromptResponse.create(total=0, current=10)
            
        # Test negative total
        with self.assertRaises(ValueError):
            ProgressPromptResponse.create(total=-1, current=5)
            
        # Test negative current
        with self.assertRaises(ValueError):
            ProgressPromptResponse.create(total=10, current=-1)
            
        # Test width less than 1
        with self.assertRaises(ValueError):
            ProgressPromptResponse.create(total=10, current=5, width=0)
            
    def _strip_ansi(self, text: str) -> str:
        """Remove ANSI color codes from text."""
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)
