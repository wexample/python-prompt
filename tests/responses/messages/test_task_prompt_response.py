"""Tests for TaskPromptResponse."""
import unittest

from wexample_prompt.responses.messages.task_prompt_response import TaskPromptResponse
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.common.prompt_context import PromptContext


class TestTaskPromptResponse(unittest.TestCase):
    """Test cases for TaskPromptResponse."""
    
    def test_create_task(self):
        """Test task message creation."""
        message = "Test task message"
        response = TaskPromptResponse.create_task(message)
        rendered = response.render()
        
        # Check message content
        self.assertIn(message, rendered)
        self.assertIn("⚡", rendered)  # Task symbol
        
    def test_message_type(self):
        """Test task message type."""
        response = TaskPromptResponse.create_task("Test")
        self.assertEqual(response.get_message_type(), MessageType.TASK)
        
    def test_multiline_task(self):
        """Test multiline task message."""
        message = "Line 1\nLine 2"
        response = TaskPromptResponse.create_task(message)
        rendered = response.render()
        
        # Check both lines are present
        self.assertIn("Line 1", rendered)
        self.assertIn("Line 2", rendered)
        
    def test_task_with_status(self):
        """Test task message with status information."""
        task = "Database backup"
        status = "In Progress"
        message = f"{task} - {status}"
        
        response = TaskPromptResponse.create_task(message)
        rendered = response.render()
        
        self.assertIn(task, rendered)
        self.assertIn(status, rendered)
        
    def test_empty_task(self):
        """Test task message with empty string."""
        response = TaskPromptResponse.create_task("")
        rendered = response.render()
        self.assertIn("⚡", rendered)
        
    def test_task_with_context(self):
        """Test task message with context."""
        message = "Processing item {item_id} of {total}"
        context = PromptContext(params={"item_id": "5", "total": "10"})
        response = TaskPromptResponse.create_task(message, context=context)
        rendered = response.render()
        self.assertIn("Processing item", rendered)
        self.assertIn("5", rendered)
        self.assertIn("10", rendered)
