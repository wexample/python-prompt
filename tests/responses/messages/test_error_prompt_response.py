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
        response = ErrorPromptResponse.create_error("Test error")
        rendered = response.render()
        self.assertIn("Test error", rendered)
        self.assertIn("❌", rendered)  # Error symbol
        
    def test_error_with_params(self):
        """Test error message with parameters."""
        context = ErrorContext(
            params={"code": "404", "message": "Not Found"}
        )
        response = ErrorPromptResponse.create_error(
            "Error {code}: {message}",
            context=context
        )
        rendered = response.render()
        self.assertIn("Error 404: Not Found", rendered)
        
    def test_error_with_trace(self):
        """Test error message with stack trace."""
        try:
            raise ValueError("Test error")
        except ValueError as e:
            context = ErrorContext(trace=True)
            response = ErrorPromptResponse.create_error(
                "An error occurred",
                context=context,
                exception=e
            )
            rendered = response.render()
            self.assertIn("An error occurred", rendered)
            self.assertIn("ValueError: Test error", rendered)
            self.assertIn("test_error_with_trace", rendered)
            
    @patch('sys.exit')
    def test_fatal_error(self, mock_exit):
        """Test fatal error handling."""
        context = ErrorContext(fatal=True, exit_code=2)
        response = ErrorPromptResponse.create_error("Fatal error", context=context)
        rendered = response.render()
        self.assertIn("Fatal error", rendered)
        
    def test_message_type(self):
        """Test error message type."""
        response = ErrorPromptResponse.create_error("Test")
        self.assertEqual(response.get_message_type(), MessageType.ERROR)
        
    def test_error_with_exception(self):
        """Test error with exception handling."""
        exception = ValueError("Custom error")
        response = ErrorPromptResponse.create_error(
            "Error occurred",
            exception=exception
        )
        self.assertEqual(response.exception, exception)
