"""Tests for WarningPromptResponse."""
import unittest

from wexample_prompt.responses.messages.warning_prompt_response import WarningPromptResponse
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.common.error_context import ErrorContext


class TestWarningPromptResponse(unittest.TestCase):
    """Test cases for WarningPromptResponse."""
    
    def test_create_warning(self):
        """Test warning message creation."""
        message = "Test warning message"
        response = WarningPromptResponse.create(message)
        rendered = response.render()
        
        # Check message content
        self.assertIn(message, rendered)
        self.assertIn("⚠", rendered)  # Warning symbol
        
    def test_message_type(self):
        """Test warning message type."""
        response = WarningPromptResponse.create("Test")
        self.assertEqual(response.get_message_type(), MessageType.WARNING)
        
    def test_multiline_warning(self):
        """Test multiline warning message."""
        message = "Line 1\nLine 2"
        response = WarningPromptResponse.create(message)
        rendered = response.render()
        
        # Check both lines are present
        self.assertIn("Line 1", rendered)
        self.assertIn("Line 2", rendered)
        
    def test_warning_with_context(self):
        """Test warning message with error context."""
        context = ErrorContext(
            params={"component": "cache", "issue": "outdated"},
            trace=True
        )
        message = "Warning in {component}: {issue}"
        
        response = WarningPromptResponse.create(
            message,
            context=context
        )
        rendered = response.render()
        
        self.assertIn("Warning in cache: outdated", rendered)
        
    def test_warning_with_stack_trace(self):
        """Test warning message with stack trace."""
        try:
            raise ValueError("Test warning")
        except ValueError:
            context = ErrorContext(trace=True)
            response = WarningPromptResponse.create(
                "A warning occurred",
                context=context
            )
            rendered = response.render()
            
            self.assertIn("A warning occurred", rendered)
            self.assertIn("ValueError: Test warning", rendered)
            self.assertIn("test_warning_with_stack_trace", rendered)
            
    def test_empty_warning(self):
        """Test warning message with empty string."""
        response = WarningPromptResponse.create("")
        rendered = response.render()
        self.assertIn("⚠", rendered)  # Should still show the warning symbol
