"""Tests for ErrorPromptResponse."""
from typing import Type
from unittest.mock import patch

from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.responses.messages.error_prompt_response import ErrorPromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest
from wexample_prompt.common.error_context import ErrorContext


class TestErrorPromptResponse(AbstractPromptResponseTest):
    """Test cases for ErrorPromptResponse."""

    def get_response_class(self) -> Type[AbstractPromptResponse]:
        return ErrorPromptResponse

    def create_test_response(self, text: str, **kwargs) -> AbstractPromptResponse:
        context = kwargs.pop('context', ErrorContext(**self.context.model_dump()))
        return ErrorPromptResponse.create_error(
            message=text,
            context=context,
            **kwargs
        )

    def get_io_method_name(self) -> str:
        return 'error'

    def _assert_specific_format(self, rendered: str):
        # Error messages should have the error symbol
        self.assert_contains_text(rendered, "❌")

    def get_expected_lines(self) -> int:
        return 1  # Error messages are single line

    def test_message_type(self):
        response = self.create_test_response(self.test_message)
        self.assertEqual(response.get_message_type(), MessageType.ERROR)

    def test_error_with_params(self):
        context = ErrorContext(
            params={"code": "404", "message": "Not Found"}
        )
        response = self.create_test_response(
            "Error {code}: {message}",
            context=context
        )
        rendered = response.render()
        self.assert_contains_text(rendered, "Error 404: Not Found")

    @patch('sys.exit')
    def test_fatal_error(self, mock_exit):
        """Test fatal error handling."""
        context = ErrorContext(is_fatal=True, exit_code=2)
        response = self.create_test_response("Fatal error", context=context)
        rendered = response.render()
        self.assert_contains_text(rendered, "Fatal error")

    def test_error_with_exception(self):
        """Test error with exception handling."""
        exception = ValueError("Custom error")
        response = self.create_test_response(
            "Error occurred",
            exception=exception
        )
        self.assertEqual(response.exception, exception)
