"""Tests for SuccessPromptResponse."""
import unittest

from wexample_prompt.responses.messages.success_prompt_response import SuccessPromptResponse
from wexample_prompt.enums.message_type import MessageType


class TestSuccessPromptResponse(unittest.TestCase):
    """Test cases for SuccessPromptResponse."""
    
    def test_create_success(self):
        """Test success message creation."""
        message = "Test success message"
        response = SuccessPromptResponse.create(message)
        rendered = response.render()
        
        # Check message content
        self.assertIn(message, rendered)
        self.assertIn("✅", rendered)  # Success symbol
        
    def test_message_type(self):
        """Test success message type."""
        response = SuccessPromptResponse.create("Test")
        self.assertEqual(response.get_message_type(), MessageType.SUCCESS)
        
    def test_multiline_success(self):
        """Test multiline success message."""
        message = "Line 1\nLine 2"
        response = SuccessPromptResponse.create(message)
        rendered = response.render()
        
        # Check both lines are present
        self.assertIn("Line 1", rendered)
        self.assertIn("Line 2", rendered)
        
    def test_success_with_details(self):
        """Test success message with operation details."""
        operation = "File upload"
        details = "3 files processed"
        message = f"{operation}: {details}"
        
        response = SuccessPromptResponse.create(message)
        rendered = response.render()
        
        self.assertIn(operation, rendered)
        self.assertIn(details, rendered)
        
    def test_empty_success(self):
        """Test success message with empty string."""
        response = SuccessPromptResponse.create("")
        rendered = response.render()
        self.assertIn("✅", rendered)  # Should still show the success symbol
