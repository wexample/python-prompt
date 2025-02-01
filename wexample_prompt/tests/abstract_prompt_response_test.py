"""Base class for testing prompt responses."""
import unittest
from abc import ABC, abstractmethod
from typing import Type
from unittest.mock import patch

from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.example.example_class_with_context import ExampleClassWithContext
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse


class AbstractPromptResponseTest(unittest.TestCase, ABC):
    """Base class for testing prompt responses.
    
    This class provides common functionality for testing prompt responses at three levels:
    1. Response class behavior
    2. IoManager integration
    3. PromptContext implementation
    """

    def setUp(self):
        """Set up common test fixtures."""
        self.terminal_width = 80
        self.context = PromptContext(terminal_width=self.terminal_width)
        self.io_manager = IoManager(terminal_width=self.terminal_width)
        self.test_message = "Test message"

    def assert_common_response_structure(self, rendered: str, expected_lines: int = 3):
        """Assert common structure for rendered responses."""
        lines = rendered.split("\n")
        self.assertEqual(len(lines), expected_lines)

        # First and last lines should be empty
        self.assertEqual(lines[0].strip(), "")
        self.assertEqual(lines[-1].strip(), "")

    def assert_contains_text(self, rendered: str, text: str):
        """Assert that rendered output contains specific text."""
        self.assertIn(text, rendered)

    @patch('wexample_prompt.common.color_manager.ColorManager.supports_color')
    def create_colored_test_context(self, mock_supports_color, color_enabled: bool = True):
        """Create a test context with color support controlled."""
        mock_supports_color.return_value = color_enabled
        return self.context

    @abstractmethod
    def get_response_class(self) -> Type[AbstractPromptResponse]:
        """Return the response class to test."""
        pass

    @abstractmethod
    def create_response(self, text: str, **kwargs) -> AbstractPromptResponse:
        """Create a response instance."""
        pass

    @abstractmethod
    def get_io_method_name(self) -> str:
        """Return the name of the IoManager method for this response type."""
        pass

    @abstractmethod
    def _assert_specific_format(self, rendered: str):
        """Assert format specific to this response type."""
        pass

    def test_response_class(self):
        """Test response class behavior."""
        response = self.create_response(self.test_message)
        rendered = response.render()

        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.test_message)
        self._assert_specific_format(rendered)

    def test_io_manager(self):
        """Test IoManager integration."""
        response = getattr(self.io_manager, self.get_io_method_name())(self.test_message)
        rendered = response.render()

        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.test_message)
        self.assertIsInstance(response, self.get_response_class())

    def test_prompt_context(self):
        """Test PromptContext implementation."""
        test_context = ExampleClassWithContext(io_manager=self.io_manager)
        response = getattr(test_context, self.get_io_method_name())(self.test_message)
        rendered = response.render()

        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.test_message)
        self.assertIsInstance(response, self.get_response_class())

    @patch('wexample_prompt.common.color_manager.ColorManager.supports_color')
    def test_custom_color(self, mock_supports_color):
        """Test response with custom color."""
        context = self.create_colored_test_context(mock_supports_color)
        from wexample_prompt.enums.terminal_color import TerminalColor

        response = self.create_response(self.test_message, context=context, color=TerminalColor.GREEN)
        rendered = response.render()

        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.test_message)
        self.assertIn("\033[", rendered)  # ANSI color code

    def test_custom_fill_char(self):
        """Test response with custom fill character."""
        fill_char = "."
        response = self.create_response(self.test_message, fill_char=fill_char)
        rendered = response.render()

        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.test_message)
        self.assertIn(fill_char, rendered)

    def test_no_color(self):
        """Test response without color."""
        response = self.create_response(self.test_message, color=None)
        rendered = response.render()

        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.test_message)
        self.assertNotIn("\033[", rendered)  # No ANSI color codes
