"""Tests for InfoPromptResponse."""
import unittest

from wexample_prompt.responses.messages.info_prompt_response import InfoPromptResponse
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.common.prompt_context import PromptContext


class TestInfoPromptResponse(unittest.TestCase):
    """Test cases for InfoPromptResponse."""
    
    def test_create_info(self):
        """Test info message creation."""
        message = "Test info message"
        response = InfoPromptResponse.create_info(message)
        rendered = response.render()
        
        # Check message content
        self.assertIn(message, rendered)
        self.assertIn("ℹ", rendered)  # Info symbol
        
    def test_message_type(self):
        """Test info message type."""
        response = InfoPromptResponse.create_info("Test")
        self.assertEqual(response.get_message_type(), MessageType.INFO)
        
    def test_multiline_info(self):
        """Test multiline info message."""
        message = "Line 1\nLine 2"
        response = InfoPromptResponse.create_info(message)
        rendered = response.render()
        
        # Check both lines are present
        self.assertIn("Line 1", rendered)
        self.assertIn("Line 2", rendered)
        
    def test_info_with_formatting(self):
        """Test info message with special formatting."""
        message = "Status: {status}\nTime: {time}"
        formatted = message.format(status="Active", time="12:00")
        
        response = InfoPromptResponse.create_info(formatted)
        rendered = response.render()
        
        self.assertIn("Status: Active", rendered)
        self.assertIn("Time: 12:00", rendered)
        
    def test_empty_info(self):
        """Test info message with empty string."""
        response = InfoPromptResponse.create_info("")
        rendered = response.render()
        self.assertIn("ℹ", rendered)  # Should still show the info symbol
        
    def test_info_with_context(self):
        """Test info message with context."""
        message = "System status: {status}"
        context = PromptContext(params={"status": "online"})
        response = InfoPromptResponse.create_info(
            message,
            context=context
        )
        rendered = response.render()
        self.assertIn("System status", rendered)
        self.assertIn("online", rendered)
