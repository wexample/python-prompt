"""Tests for InfoPromptResponse."""
from typing import Type
import unittest

from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.responses.messages.info_prompt_response import InfoPromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest


class TestInfoPromptResponse(AbstractPromptResponseTest):
    """Test cases for InfoPromptResponse."""

    def get_response_class(self) -> Type[AbstractPromptResponse]:
        return InfoPromptResponse

    def create_test_response(self, text: str, **kwargs) -> AbstractPromptResponse:
        context = kwargs.pop('context', self.context)
        return InfoPromptResponse.create_info(
            message=text,
            context=context,
            **kwargs
        )

    def get_io_method_name(self) -> str:
        return 'info'

    def _assert_specific_format(self, rendered: str):
        self.assertIn("ℹ️", rendered)  # Info symbol

    def get_expected_lines(self) -> int:
        return 1  # Info messages are single line

    @unittest.skip("Info messages do not support custom fill characters")
    def test_custom_fill_char(self):
        pass

    def test_message_type(self):
        response = self.create_test_response(self.test_message)
        self.assertEqual(response.get_message_type(), MessageType.INFO)

    def test_multiline_info(self):
        message = "Line 1\nLine 2"
        response = self.create_test_response(message)
        rendered = response.render()

        self.assert_contains_text(rendered, "Line 1")
        self.assert_contains_text(rendered, "Line 2")

    def test_info_with_formatting(self):
        message = "Status: {status}\nTime: {time}"
        formatted = message.format(status="Active", time="12:00")

        response = self.create_test_response(formatted)
        rendered = response.render()

        self.assert_contains_text(rendered, "Status: Active")
        self.assert_contains_text(rendered, "Time: 12:00")
