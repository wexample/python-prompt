"""Tests for FailurePromptResponse."""
from typing import Type

from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.responses.messages.failure_prompt_response import FailurePromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest


class TestFailurePromptResponse(AbstractPromptResponseTest):
    """Test cases for FailurePromptResponse."""

    def get_response_class(self) -> Type[AbstractPromptResponse]:
        return FailurePromptResponse

    def create_test_response(self, text: str, **kwargs) -> AbstractPromptResponse:
        context = kwargs.pop('context', self.context)
        return FailurePromptResponse.create_failure(
            message=text,
            context=context,
            **kwargs
        )

    def get_io_method_name(self) -> str:
        return 'failure'

    def _assert_specific_format(self, rendered: str):
        # Failure messages should have the failure symbol
        self.assert_contains_text(rendered, "❌")

    def get_expected_lines(self) -> int:
        return 1  # Failure messages are single line

    def test_message_type(self):
        response = self.create_test_response(self.test_message)
        self.assertEqual(response.get_message_type(), MessageType.FAILURE)

    def test_multiline_failure(self):
        message = "Line 1\nLine 2"
        response = self.create_test_response(message)
        rendered = response.render()

        self.assert_contains_text(rendered, "Line 1")
        self.assert_contains_text(rendered, "Line 2")

    def test_failure_with_details(self):
        main_message = "Operation failed"
        details = "Connection timeout after 30 seconds"
        message = f"{main_message}: {details}"

        response = self.create_test_response(message)
        rendered = response.render()

        self.assert_contains_text(rendered, main_message)
        self.assert_contains_text(rendered, details)

    def test_empty_failure(self):
        response = self.create_test_response("")
        rendered = response.render()
        self.assert_contains_text(rendered, "❌")

    def test_failure_with_context(self):
        message = "Operation failed: {error_code}"
        self.context.params = {"error_code": "500"}
        response = self.create_test_response(message)
        rendered = response.render()
        self.assert_contains_text(rendered, "Operation failed")
        self.assert_contains_text(rendered, "500")
