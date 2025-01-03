"""Tests for IOManager."""
import io
import sys
import unittest

from wexample_prompt.io_manager import IOManager
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.responses.messages.success_prompt_response import SuccessPromptResponse
from wexample_prompt.responses.messages.error_prompt_response import ErrorPromptResponse
from wexample_prompt.common.color_manager import ColorManager
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.responses.base_prompt_response import BasePromptResponse


class TestIOManager(unittest.TestCase):
    """Test cases for IOManager."""
    
    def setUp(self):
        """Set up test cases."""
        # Mock stdout with StringIO
        self.stdout = io.StringIO()
        sys.stdout = self.stdout
        self.io_manager = IOManager()
        self.io_manager._stdout = self.stdout
        
        # Force color support for tests
        self.original_supports_color = ColorManager.supports_color
        ColorManager.supports_color = lambda: True
    
    def tearDown(self):
        """Clean up after tests."""
        sys.stdout = sys.__stdout__
        self.stdout.close()
        # Restore original color support check
        ColorManager.supports_color = self.original_supports_color
    
    def test_print_responses(self):
        """Test printing multiple responses."""
        # Create test responses
        responses = [
            SuccessPromptResponse.create("Success"),
            ErrorPromptResponse.create("Error")
        ]
        
        # Print responses
        self.io_manager.print_responses(responses)
        
        # Check output
        output = self.stdout.getvalue()
        self.assertIn("Success", output)
        self.assertIn("Error", output)
    
    def test_indentation(self):
        """Test indentation functionality."""
        # Create a test response with a simple text segment
        line = PromptResponseLine(segments=[
            PromptResponseSegment(text="Test message")
        ])
        response = BasePromptResponse(
            lines=[line],
            message_type=MessageType.SUCCESS
        )
        
        # Set indentation level to 2 (4 spaces)
        self.io_manager._log_indent = 2
        
        # Print response
        self.io_manager.print_response(response)
        
        # Check output has correct indentation (4 spaces)
        output = self.stdout.getvalue()
        self.assertTrue(any(line.startswith("    ") for line in output.splitlines()))

    def test_theme_color_application(self):
        """Test that theme colors are properly applied."""
        # Create a test response
        response = SuccessPromptResponse.create("Test message")
        
        # Print response
        self.io_manager.print_response(response)
        
        # Check output contains color codes
        output = self.stdout.getvalue()
        self.assertIn("\033[", output)  # ANSI color code
        self.assertIn("Test message", output)
