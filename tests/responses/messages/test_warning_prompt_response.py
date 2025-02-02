"""Tests for WarningPromptResponse."""
from typing import Type

from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.responses.messages.warning_prompt_response import WarningPromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest
from wexample_prompt.common.error_context import ErrorContext


class TestWarningPromptResponse(AbstractPromptResponseTest):
    """Test cases for WarningPromptResponse."""

    def get_response_class(self) -> Type[AbstractPromptResponse]:
        return WarningPromptResponse

    def create_test_response(self, text: str, **kwargs) -> AbstractPromptResponse:
        context = kwargs.pop('context', self.context)
        return WarningPromptResponse.create_warning(
            message=text,
            context=context,
            **kwargs
        )

    def get_io_method_name(self) -> str:
        return 'warning'

    def _assert_specific_format(self, rendered: str):
        # Warning messages should have the warning symbol
        self.assert_contains_text(rendered, "⚠️")

    def get_expected_lines(self) -> int:
        return 1  # Warning messages are single line

    def test_message_type(self):
        response = self.create_test_response(self.test_message)
        self.assertEqual(response.get_message_type(), MessageType.WARNING)

    def test_multiline_warning(self):
        message = "Line 1\nLine 2"
        response = self.create_test_response(message)
        rendered = response.render()

        self.assert_contains_text(rendered, "Line 1")
        self.assert_contains_text(rendered, "Line 2")

    def test_warning_with_error_context(self):
        message = "Warning in {component}: {issue}"
        context = ErrorContext(
            params={"component": "cache", "issue": "outdated"},
        )

        response = self.create_test_response(message, context=context)
        rendered = response.render()
        self.assert_contains_text(rendered, "Warning in cache: outdated")

    def test_empty_warning(self):
        response = self.create_test_response("")
        rendered = response.render()
        self.assert_contains_text(rendered, "⚠️")
