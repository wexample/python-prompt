"""Tests for ErrorPromptResponse."""
import unittest
from unittest.mock import patch

from wexample_prompt.responses.messages.error_prompt_response import ErrorPromptResponse
from wexample_prompt.common.error_context import ErrorContext
from wexample_prompt.enums.message_type import MessageType


class TestErrorPromptResponse(unittest.TestCase):
    """Test cases for ErrorPromptResponse."""
    
    def test_basic_error(self):
        """Test basic error message."""
        response = ErrorPromptResponse.create("Test error")
        rendered = response.render()
        self.assertIn("Test error", rendered)
        self.assertIn("❌", rendered)  # Error symbol
        
    def test_error_with_params(self):
        """Test error message with parameters."""
        context = ErrorContext(
            params={"code": "404", "message": "Not Found"}
        )
        response = ErrorPromptResponse.create(
            "Error {code}: {message}",
            context=context
        )
        rendered = response.render()
        self.assertIn("Error 404: Not Found", rendered)
        
    def test_error_with_trace(self):
        """Test error message with stack trace."""
        try:
            raise ValueError("Test error")
        except ValueError:
            context = ErrorContext(trace=True)
            response = ErrorPromptResponse.create(
                "An error occurred",
                context=context
            )
            rendered = response.render()
            self.assertIn("An error occurred", rendered)
            self.assertIn("ValueError: Test error", rendered)
            self.assertIn("test_error_with_trace", rendered)
            
    @patch('sys.exit')
    def test_fatal_error(self, mock_exit):
        """Test fatal error handling."""
        context = ErrorContext(fatal=True, exit_code=2)
        ErrorPromptResponse.create("Fatal error", context=context)
        mock_exit.assert_called_once_with(2)
        
    def test_message_type(self):
        """Test error message type."""
        response = ErrorPromptResponse.create("Test error")
        self.assertEqual(response.get_message_type(), MessageType.ERROR)
