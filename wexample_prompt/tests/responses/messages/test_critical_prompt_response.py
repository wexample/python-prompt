"""Tests for CriticalPromptResponse."""
import unittest

from wexample_prompt.responses.messages.critical_prompt_response import CriticalPromptResponse
from wexample_prompt.enums.message_type import MessageType


class TestCriticalPromptResponse(unittest.TestCase):
    """Test cases for CriticalPromptResponse."""
    
    def test_create_critical(self):
        """Test critical message creation."""
        message = "Test critical message"
        response = CriticalPromptResponse.create(message)
        rendered = response.render()
        
        # Check message content
        self.assertIn(message, rendered)
        self.assertIn("🔥", rendered)  # Critical symbol
        
    def test_message_type(self):
        """Test critical message type."""
        response = CriticalPromptResponse.create("Test")
        self.assertEqual(response.get_message_type(), MessageType.CRITICAL)
        
    def test_multiline_critical(self):
        """Test multiline critical message."""
        message = "Line 1\nLine 2"
        response = CriticalPromptResponse.create(message)
        rendered = response.render()
        
        # Check both lines are present
        self.assertIn("Line 1", rendered)
        self.assertIn("Line 2", rendered)
