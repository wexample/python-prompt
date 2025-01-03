"""Tests for IOManager class."""
import io
import sys
from unittest import TestCase
from unittest.mock import MagicMock, patch

from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.io_manager import IOManager
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.responses.messages.success_prompt_response import SuccessPromptResponse
from wexample_prompt.responses.messages.error_prompt_response import ErrorPromptResponse


class TestIOManager(TestCase):
    """Test cases for IOManager."""

    def setUp(self):
        """Set up test cases."""
        self.io_manager = IOManager()
        # Capture stdout
        self.stdout = io.StringIO()
        sys.stdout = self.stdout

    def tearDown(self):
        """Clean up after tests."""
        sys.stdout = sys.__stdout__
        self.stdout.close()

    def test_print_responses(self):
        """Test printing multiple responses."""
        # Create test responses
        success = SuccessPromptResponse.create("Success message")
        error = ErrorPromptResponse.create("Error message")
        
        # Print responses
        self.io_manager.print_responses([success, error])
        
        # Check output
        output = self.stdout.getvalue()
        self.assertIn("Success message", output)
        self.assertIn("Error message", output)

    def test_print_response_line(self):
        """Test printing a single response line."""
        # Create a test line
        segment = PromptResponseSegment(text="Test message")
        line = PromptResponseLine(
            segments=[segment],
            line_type=MessageType.SUCCESS
        )
        response = SuccessPromptResponse.create("Test")
        
        # Print line
        self.io_manager.print_response_line(line, response)
        
        # Check output
        self.assertIn("Test message", self.stdout.getvalue())

    def test_indentation(self):
        """Test indentation functionality."""
        # Create a test response
        response = SuccessPromptResponse.create("Test message")
        
        # Set indentation
        self.io_manager.indent_level = 2
        
        # Print response
        self.io_manager.print_response(response)
        
        # Check output has correct indentation
        output = self.stdout.getvalue()
        self.assertTrue(output.startswith("    "))  # 2 levels = 4 spaces

    @patch('shutil.get_terminal_size')
    def test_terminal_width(self, mock_get_terminal_size):
        """Test terminal width handling."""
        # Mock terminal size
        mock_get_terminal_size.return_value = MagicMock(columns=100)
        
        # Create new IOManager
        io_manager = IOManager()
        
        # Check terminal width
        self.assertEqual(io_manager._tty_width, 100)

    def test_theme_color_application(self):
        """Test that theme colors are properly applied."""
        # Create a test response
        response = SuccessPromptResponse.create("Test message")
        
        # Print response
        self.io_manager.print_response(response)
        
        # Check output contains color codes
        output = self.stdout.getvalue()
        self.assertIn("\033[", output)  # ANSI color code
        self.assertIn("\033[0m", output)  # Color reset
