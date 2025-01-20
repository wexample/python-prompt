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
        response = WarningPromptResponse.create_warning(message)
        rendered = response.render()
        
        # Check message content
        self.assertIn(message, rendered)
        self.assertIn("⚠", rendered)  # Warning symbol
        
    def test_message_type(self):
        """Test warning message type."""
        response = WarningPromptResponse.create_warning("Test")
        self.assertEqual(response.get_message_type(), MessageType.WARNING)
        
    def test_multiline_warning(self):
        """Test multiline warning message."""
        message = "Line 1\nLine 2"
        response = WarningPromptResponse.create_warning(message)
        rendered = response.render()
        
        # Check both lines are present
        self.assertIn("Line 1", rendered)
        self.assertIn("Line 2", rendered)
        
    def test_warning_with_context(self):
        """Test warning message with error context."""
        message = "Warning in {component}: {issue}"
        context = ErrorContext(
            params={"component": "cache", "issue": "outdated"},
        )
        
        response = WarningPromptResponse.create_warning(
            message,
            context=context
        )
        rendered = response.render()
        self.assertIn("Warning in cache: outdated", rendered)
        
    def test_warning_without_context(self):
        """Test warning message without context."""
        message = "Simple warning"
        response = WarningPromptResponse.create_warning(message)
        rendered = response.render()
        self.assertIn(message, rendered)
        
    def test_empty_warning(self):
        """Test warning message with empty string."""
        response = WarningPromptResponse.create_warning("")
        rendered = response.render()
        self.assertIn("⚠", rendered)
