"""Tests for TaskPromptResponse."""
from typing import Type

from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.responses.messages.task_prompt_response import TaskPromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest


class TestTaskPromptResponse(AbstractPromptResponseTest):
    """Test cases for TaskPromptResponse."""

    def get_response_class(self) -> Type[AbstractPromptResponse]:
        return TaskPromptResponse

    def create_test_response(self, text: str, **kwargs) -> AbstractPromptResponse:
        context = kwargs.pop('context', self.context)
        return TaskPromptResponse.create_task(
            message=text,
            context=context,
            **kwargs
        )

    def get_io_method_name(self) -> str:
        return 'task'

    def _assert_specific_format(self, rendered: str):
        # Task messages should have the task symbol
        self.assert_contains_text(rendered, "⚡")

    def get_expected_lines(self) -> int:
        return 1  # Task messages are single line

    def test_message_type(self):
        response = self.create_test_response(self.test_message)
        self.assertEqual(response.get_message_type(), MessageType.TASK)

    def test_multiline_task(self):
        message = "Line 1\nLine 2"
        response = self.create_test_response(message)
        rendered = response.render()

        self.assert_contains_text(rendered, "Line 1")
        self.assert_contains_text(rendered, "Line 2")

    def test_task_with_status(self):
        task = "Database backup"
        status = "In Progress"
        message = f"{task} - {status}"

        response = self.create_test_response(message)
        rendered = response.render()

        self.assert_contains_text(rendered, task)
        self.assert_contains_text(rendered, status)

    def test_empty_task(self):
        response = self.create_test_response("")
        rendered = response.render()
        self.assert_contains_text(rendered, "⚡")

    def test_task_with_context(self):
        message = "Files processed: {count} files"
        self.context.params = {"count": "3"}
        response = self.create_test_response(message)
        rendered = response.render()
        self.assert_contains_text(rendered, "Files processed")
        self.assert_contains_text(rendered, "3")
