"""Tests for ErrorContext."""
import unittest

from wexample_prompt.common.error_context import ErrorContext


class TestErrorContext(unittest.TestCase):
    """Test cases for ErrorContext."""
    
    def test_default_values(self):
        """Test default values are set correctly."""
        context = ErrorContext()
        self.assertFalse(context.fatal)
        self.assertTrue(context.trace)
        self.assertIsNone(context.params)
    
    def test_custom_values(self):
        """Test custom values are set correctly."""
        context = ErrorContext(
            fatal=True,
            trace=False,
            params={"key": "value"}
        )
        self.assertTrue(context.fatal)
        self.assertFalse(context.trace)
        self.assertEqual(context.params, {"key": "value"})
    
    def test_format_message_without_params(self):
        """Test message formatting without parameters."""
        context = ErrorContext()
        message = "Simple message"
        formatted = context.format_message(message)
        self.assertEqual(formatted, message)
    
    def test_format_message_with_params(self):
        """Test message formatting with parameters."""
        context = ErrorContext(params={
            "name": "test",
            "value": 42
        })
        message = "Name: {name}, Value: {value}"
        formatted = context.format_message(message)
        self.assertEqual(formatted, "Name: test, Value: 42")
