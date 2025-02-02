"""Tests for progress prompt responses."""
from typing import Type
from unittest.mock import patch
import time

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.example.example_class_with_context import ExampleClassWithContext
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.responses.interactive.progress_prompt_response import ProgressPromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest
from wexample_prompt.progress.step_progress_context import ProgressStep


class TestProgressPromptResponse(AbstractPromptResponseTest):
    """Test cases for ProgressPromptResponse."""

    def setUp(self):
        """Set up test cases."""
        super().setUp()
        self.total = 10
        self.current = 5
        self.width = 20
        self.label = "Processing..."

    def get_response_class(self) -> Type[AbstractPromptResponse]:
        return ProgressPromptResponse

    def create_test_response(self, text: str, **kwargs) -> AbstractPromptResponse:
        context = kwargs.pop('context', self.context)
        return ProgressPromptResponse.create_progress(
            total=self.total,
            current=self.current,
            width=self.width,
            label=text,
            context=context,
            **kwargs
        )

    def get_io_method_name(self) -> str:
        return 'progress'

    def _assert_specific_format(self, rendered: str):
        # Progress bars should have percentage and progress indicators
        self.assert_contains_text(rendered, "%")
        self.assert_contains_text(rendered, ProgressPromptResponse.FILL_CHAR)
        self.assert_contains_text(rendered, ProgressPromptResponse.EMPTY_CHAR)

    def get_expected_lines(self) -> int:
        return 1  # Progress bar is single line

    def test_create_progress(self):
        """Test creating progress bar response."""
        response = self.create_test_response(self.test_message)

        rendered = response.render()
        self.assert_contains_text(rendered, self.test_message)
        self.assert_contains_text(rendered, "50%")  # 5/10 = 50%

    def test_invalid_values(self):
        """Test invalid progress values."""
        with self.assertRaises(ValueError):
            ProgressPromptResponse.create_progress(total=0, current=0)
        with self.assertRaises(ValueError):
            ProgressPromptResponse.create_progress(total=10, current=-1)
        with self.assertRaises(ValueError):
            ProgressPromptResponse.create_progress(total=10, current=5, width=0)

    def test_custom_style(self):
        """Test customizing progress bar style."""
        old_fill = ProgressPromptResponse.FILL_CHAR
        old_empty = ProgressPromptResponse.EMPTY_CHAR

        try:
            ProgressPromptResponse.set_style(fill_char="#", empty_char="-")
            response = self.create_test_response(self.test_message)
            rendered = response.render()
            
            self.assert_contains_text(rendered, "#")
            self.assert_contains_text(rendered, "-")
        finally:
            # Restore original style
            ProgressPromptResponse.set_style(fill_char=old_fill, empty_char=old_empty)

    def test_io_manager(self):
        """Test IoManager integration."""
        result = self.io_manager.progress(
            total=self.total,
            current=self.current,
            width=self.width,
            label=self.test_message
        )

        # Verify that we get a ProgressPromptResponse object
        self.assertIsInstance(result, ProgressPromptResponse)

    def test_prompt_context(self):
        """Test PromptContext implementation."""
        context = self.context
        class_with_context = ExampleClassWithContext(
            context=context,
            io_manager=self.io_manager
        )
        result = class_with_context.progress(
            total=self.total,
            current=self.current,
            width=self.width,
            label=self.test_message
        )

        # Verify that we get a ProgressPromptResponse object
        self.assertIsInstance(result, ProgressPromptResponse)

    def test_progress_steps(self):
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
