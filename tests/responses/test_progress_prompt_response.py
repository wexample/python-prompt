"""Tests for ProgressPromptResponse."""
import unittest
import re

from wexample_prompt.responses.progress_prompt_response import ProgressPromptResponse
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.progress.step_progress_context import ProgressStep


class TestProgressPromptResponse(unittest.TestCase):
    """Test cases for ProgressPromptResponse."""
    
    def setUp(self):
        """Set up test cases."""
        self.context = PromptContext(terminal_width=80)
        # Use simple characters for testing
        ProgressPromptResponse.set_style(fill_char="=", empty_char="-")
        
    def test_create_progress(self):
        """Test progress bar creation."""
        progress = ProgressPromptResponse.create_progress(
            total=100,
            current=50,
            context=self.context
        )
        rendered = self._strip_ansi(progress.render())
        
        # Check basic structure
        self.assertIn("=", rendered)  # Progress indicator
        self.assertIn("-", rendered)  # Empty indicator
        self.assertIn("50%", rendered)  # Percentage
        
    def test_zero_progress(self):
        """Test progress bar at 0%."""
        progress = ProgressPromptResponse.create_progress(
            total=100,
            current=0,
            context=self.context
        )
        rendered = self._strip_ansi(progress.render())
        self.assertTrue(rendered.startswith("-" * 50))  # Should be empty
        self.assertIn("0%", rendered)
        
    def test_full_progress(self):
        """Test progress bar at 100%."""
        progress = ProgressPromptResponse.create_progress(
            total=100,
            current=100,
            context=self.context
        )
        rendered = self._strip_ansi(progress.render())
        self.assertTrue("=" * 50 in rendered)  # Should be full
        self.assertIn("100%", rendered)
        
    def test_partial_progress(self):
        """Test progress bar with partial completion."""
        progress = ProgressPromptResponse.create_progress(
            total=10,
            current=7,
            context=self.context
        )
        rendered = self._strip_ansi(progress.render())
        self.assertIn("70%", rendered)
        
    def test_custom_width(self):
        """Test progress bar with custom width."""
        width = 20
        progress = ProgressPromptResponse.create_progress(
            total=100,
            current=50,
            width=width,
            context=self.context
        )
        rendered = self._strip_ansi(progress.render())
        self.assertEqual(len(rendered.split()[0]), width)  # Check bar width
        
    def test_with_label(self):
        """Test progress bar with label."""
        label = "Processing"
        progress = ProgressPromptResponse.create_progress(
            total=100,
            current=50,
            label=label,
            context=self.context
        )
        rendered = self._strip_ansi(progress.render())
        self.assertIn(label, rendered)
        
    def test_step_progress(self):
        """Test step-based progress."""
        def step1():
            return "Step 1 done"
            
        def step2():
            return "Step 2 done"
            
        steps = [
            ProgressStep(callback=step1, description="Step 1", weight=1),
            ProgressStep(callback=step2, description="Step 2", weight=1)
        ]
        
        with ProgressPromptResponse.create_steps(
            steps=steps,
            title="Test Steps",
            context=self.context
        ) as progress:
            results = progress.execute_steps()
                
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], "Step 1 done")
        self.assertEqual(results[1], "Step 2 done")
        
    def test_execute_callbacks(self):
        """Test executing callbacks with progress."""
        def step1():
            """First test step."""
            return "Step 1 done"
            
        def step2():
            """Second test step."""
            return "Step 2 done"
            
        results = ProgressPromptResponse.execute(
            callbacks=[step1, step2],
            title="Test Callbacks",
            context=self.context
        )
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], "Step 1 done")
        self.assertEqual(results[1], "Step 2 done")
        
    @staticmethod
    def _strip_ansi(text: str) -> str:
        """Remove ANSI color codes from text."""
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)
