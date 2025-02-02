"""Tests for progress prompt responses."""
from unittest.mock import patch

from wexample_prompt.responses.interactive.progress_prompt_response import ProgressPromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest


class TestProgressPromptResponse(AbstractPromptResponseTest):
    """Test cases for ProgressPromptResponse."""

    def test_create_progress(self):
        """Test creating a progress bar."""
        response = ProgressPromptResponse.create_progress(
            total=10,
            current=5,
            label="Processing"
        )
        self.assertIsInstance(response, ProgressPromptResponse)
        self.assertEqual(response.total, 10)
        self.assertEqual(response.current, 5)
        self.assertEqual(response.label, "Processing")

    def test_custom_style(self):
        """Test customizing progress bar style."""
        ProgressPromptResponse.set_style(fill_char="#", empty_char="-")
        self.assertEqual(ProgressPromptResponse.FILL_CHAR, "#")
        self.assertEqual(ProgressPromptResponse.EMPTY_CHAR, "-")

    def test_invalid_values(self):
        """Test invalid progress values."""
        with self.assertRaises(ValueError):
            ProgressPromptResponse.create_progress(total=0, current=0)
        with self.assertRaises(ValueError):
            ProgressPromptResponse.create_progress(total=10, current=-1)

    def test_io_manager(self):
        """Test IoManager integration."""
        result = self.io_manager.progress(
            total=10,
            current=5,
            label=self.test_message
        )
        self.assertIsInstance(result, ProgressPromptResponse)

    def test_progress_steps(self):
        from wexample_prompt.progress.step_progress_context import ProgressStep

        """Test progress steps creation."""
        steps = [
            ProgressStep(callback=lambda: None, description="Step 1", weight=1),
            ProgressStep(callback=lambda: None, description="Step 2", weight=2)
        ]
        context = self.io_manager.progress_steps(steps, title="Test Steps")
        self.assertEqual(context.total_weight, 3)

    @patch('time.sleep')  # Mock sleep to speed up tests
    def test_progress_execute(self, mock_sleep):
        """Test executing callbacks with progress."""
        mock_sleep.return_value = None
        callbacks = [
            lambda: "step1",
            lambda: "step2",
            lambda: "step3"
        ]
        results = self.io_manager.progress_execute(
            callbacks=callbacks,
            title="Test Execute"
        )
        self.assertEqual(len(results), 3)
        self.assertEqual(results, ["step1", "step2", "step3"])

    def test_prompt_context(self):
        from wexample_prompt.example.example_class_with_context import ExampleClassWithContext

        """Test PromptContext implementation."""
        context = self.context
        class_with_context = ExampleClassWithContext(
            context=context,
            io_manager=self.io_manager
        )
        result = class_with_context.progress(
            total=10,
            current=5,
            label=self.test_message
        )
        self.assertIsInstance(result, ProgressPromptResponse)
