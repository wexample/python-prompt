"""Tests for AlertPromptResponse."""
import unittest

from wexample_prompt.responses.messages.alert_prompt_response import AlertPromptResponse
from wexample_prompt.enums.message_type import MessageType


class TestAlertPromptResponse(unittest.TestCase):
    """Test cases for AlertPromptResponse."""
    
    def test_create_alert(self):
        """Test alert message creation."""
        message = "Test alert message"
        response = AlertPromptResponse.create(message)
        rendered = response.render()
        
        # Check message content
        self.assertIn(message, rendered)
        self.assertIn("🚨", rendered)  # Alert symbol
        
    def test_message_type(self):
        """Test alert message type."""
        response = AlertPromptResponse.create("Test")
        self.assertEqual(response.get_message_type(), MessageType.ALERT)
        
    def test_multiline_alert(self):
        """Test multiline alert message."""
        message = "Line 1\nLine 2"
        response = AlertPromptResponse.create(message)
        rendered = response.render()
        
        # Check both lines are present
        self.assertIn("Line 1", rendered)
        self.assertIn("Line 2", rendered)
