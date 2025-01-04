"""Tests for LogPromptResponse."""
import unittest

from wexample_prompt.responses.messages.log_prompt_response import LogPromptResponse
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment


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
        self.assertEqual("", rendered)

    def test_single_indentation(self):
        """Test log message with single level indentation."""
        message = "Indented message"
        response = LogPromptResponse.create(message)
        response.lines[0].indent_level = 1
        rendered = response.render()
        
        # Should have 2 spaces of indentation
        self.assertTrue(rendered.startswith("  "))
        self.assertEqual("  " + message, rendered)

    def test_multiple_indentation_levels(self):
        """Test log messages with different indentation levels."""
        messages = [
            (0, "Root level"),
            (1, "First indent"),
            (2, "Second indent"),
            (3, "Third indent"),
            (1, "Back to first"),
        ]
        
        # Create response with multiple lines at different indentation levels
        lines = []
        for indent, msg in messages:
            line = PromptResponseLine(
                segments=[PromptResponseSegment(text=msg)],
                indent_level=indent
            )
            lines.append(line)
        
        response = LogPromptResponse(lines=lines)
        rendered = response.render()
        rendered_lines = rendered.split("\n")
        
        # Verify each line has correct indentation
        for i, (indent, msg) in enumerate(messages):
            expected_spaces = "  " * indent
            self.assertEqual(rendered_lines[i], expected_spaces + msg)

    def test_indentation_with_multiline(self):
        """Test indentation with multiline messages."""
        # Create multiline message
        message = "First line\nSecond line\nThird line"
        response = LogPromptResponse.create(message)
        
        # Set different indentation for each line
        for i, line in enumerate(response.lines):
            line.indent_level = i
        
        rendered = response.render()
        lines = rendered.split('\n')
        
        # Verify progressive indentation
        self.assertEqual(lines[0], "First line")
        self.assertEqual(lines[1], "  Second line")
        self.assertEqual(lines[2], "    Third line")

    def test_zero_indentation(self):
        """Test explicit zero indentation."""
        message = "No indent"
        response = LogPromptResponse.create(message)
        response.lines[0].indent_level = 0
        rendered = response.render()
        
        # Should have no leading spaces
        self.assertEqual(message, rendered)
        self.assertFalse(rendered.startswith(" "))
