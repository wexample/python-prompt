"""Tests for LogPromptResponse."""
import unittest

from wexample_prompt.responses.messages.log_prompt_response import LogPromptResponse
from wexample_prompt.enums.message_type import MessageType


class TestLogPromptResponse(unittest.TestCase):
    """Test cases for LogPromptResponse."""
    
    def test_create_log(self):
        """Test log message creation."""
        message = "Test log message"
        response = LogPromptResponse.create(message)
        rendered = response.render()
        
        # Check message content
        self.assertIn(message, rendered)

    def test_message_type(self):
        """Test log message type."""
        response = LogPromptResponse.create("Test")
        self.assertEqual(response.get_message_type(), MessageType.LOG)
        
    def test_multiline_log(self):
        """Test multiline log message."""
        message = "Line 1\nLine 2"
        response = LogPromptResponse.create(message)
        rendered = response.render()
        
        # Check both lines are present
        self.assertIn("Line 1", rendered)
        self.assertIn("Line 2", rendered)
        
    def test_log_with_timestamp(self):
        """Test log message with timestamp."""
        timestamp = "2025-01-04 12:00:00"
        message = f"[{timestamp}] System started"
        
        response = LogPromptResponse.create(message)
        rendered = response.render()
        
        self.assertIn(timestamp, rendered)
        self.assertIn("System started", rendered)
        
    def test_log_with_level(self):
        """Test log message with log level."""
        message = "[INFO] Application initialized"
        response = LogPromptResponse.create(message)
        rendered = response.render()
        
        self.assertIn("[INFO]", rendered)
        self.assertIn("Application initialized", rendered)
        
    def test_empty_log(self):
        """Test log message with empty string."""
        response = LogPromptResponse.create("")
        rendered = response.render()
        self.assertEquals("", rendered)
