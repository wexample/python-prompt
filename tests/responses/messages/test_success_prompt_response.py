"""Tests for SuccessPromptResponse."""
from typing import Type

from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.responses.messages.success_prompt_response import SuccessPromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest


class TestSuccessPromptResponse(AbstractPromptResponseTest):
    """Test cases for SuccessPromptResponse."""

    def get_response_class(self) -> Type[AbstractPromptResponse]:
        return SuccessPromptResponse

    def create_test_response(self, text: str, **kwargs) -> AbstractPromptResponse:
        context = kwargs.pop('context', self.context)
        return SuccessPromptResponse.create_success(
            message=text,
            context=context,
            **kwargs
        )

    def get_io_method_name(self) -> str:
        return 'success'

    def _assert_specific_format(self, rendered: str):
        # Success messages should have the success symbol
        self.assert_contains_text(rendered, "✅")

    def get_expected_lines(self) -> int:
        return 1  # Success messages are single line

    def test_message_type(self):
        response = self.create_test_response(self.test_message)
        self.assertEqual(response.get_message_type(), MessageType.SUCCESS)

    def test_multiline_success(self):
        message = "Line 1\nLine 2"
        response = self.create_test_response(message)
        rendered = response.render()

        self.assert_contains_text(rendered, "Line 1")
        self.assert_contains_text(rendered, "Line 2")

    def test_success_with_details(self):
        operation = "File upload"
        details = "3 files processed"
        message = f"{operation}: {details}"

        response = self.create_test_response(message)
        rendered = response.render()

        self.assert_contains_text(rendered, operation)
        self.assert_contains_text(rendered, details)

    def test_empty_success(self):
        response = self.create_test_response("")
        rendered = response.render()
        self.assert_contains_text(rendered, "✅")

    def test_success_with_context(self):
        message = "Files processed: {count} files"
        context = self.context(params={"count": "3"})
        response = self.create_test_response(message, context=context)
        rendered = response.render()
        self.assert_contains_text(rendered, "Files processed")
        self.assert_contains_text(rendered, "3")
