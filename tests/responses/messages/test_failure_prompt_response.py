"""Tests for FailurePromptResponse."""
import unittest

from wexample_prompt.responses.messages.failure_prompt_response import FailurePromptResponse
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.common.prompt_context import PromptContext


class TestFailurePromptResponse(unittest.TestCase):
    """Test cases for FailurePromptResponse."""
    
    def test_create_failure(self):
        """Test failure message creation."""
        message = "Test failure message"
        response = FailurePromptResponse.create_failure(message)
        rendered = response.render()
        
        # Check message content
        self.assertIn(message, rendered)
        self.assertIn("❌", rendered)  # Failure symbol
        
    def test_message_type(self):
        """Test failure message type."""
        response = FailurePromptResponse.create_failure("Test")
        self.assertEqual(response.get_message_type(), MessageType.FAILURE)
        
    def test_multiline_failure(self):
        """Test multiline failure message."""
        message = "Line 1\nLine 2"
        response = FailurePromptResponse.create_failure(message)
        rendered = response.render()
        
        # Check both lines are present
        self.assertIn("Line 1", rendered)
        self.assertIn("Line 2", rendered)
        
    def test_failure_with_details(self):
        """Test failure message with detailed error information."""
        main_message = "Operation failed"
        details = "Connection timeout after 30 seconds"
        message = f"{main_message}: {details}"
        
        response = FailurePromptResponse.create_failure(message)
        rendered = response.render()
        
        self.assertIn(main_message, rendered)
        self.assertIn(details, rendered)
        
    def test_empty_failure(self):
        """Test failure message with empty string."""
        response = FailurePromptResponse.create_failure("")
        rendered = response.render()
        self.assertIn("❌", rendered)
        
    def test_failure_with_context(self):
        """Test failure message with context."""
        message = "Operation failed: {error_code}"
        context = PromptContext(params={"error_code": "500"})
        response = FailurePromptResponse.create_failure(
            message,
            context=context
        )
        rendered = response.render()
        self.assertIn("Operation failed", rendered)
        self.assertIn("500", rendered)
