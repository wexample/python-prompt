"""Tests for DebugPromptResponse."""
import unittest

from wexample_prompt.responses.messages.debug_prompt_response import DebugPromptResponse
from wexample_prompt.enums.message_type import MessageType


class TestDebugPromptResponse(unittest.TestCase):
    """Test cases for DebugPromptResponse."""
    
    def test_create_debug(self):
        """Test debug message creation."""
        message = "Test debug message"
        response = DebugPromptResponse.create(message)
        rendered = response.render()
        
        # Check message content
        self.assertIn(message, rendered)
        self.assertIn("🔍", rendered)  # Debug symbol
        
    def test_message_type(self):
        """Test debug message type."""
        response = DebugPromptResponse.create("Test")
        self.assertEqual(response.get_message_type(), MessageType.DEBUG)
        
    def test_multiline_debug(self):
        """Test multiline debug message."""
        message = "Line 1\nLine 2"
        response = DebugPromptResponse.create(message)
        rendered = response.render()
        
        # Check both lines are present
        self.assertIn("Line 1", rendered)
        self.assertIn("Line 2", rendered)
