"""Tests for DebugPromptResponse."""
from typing import Type
import unittest

from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.responses.messages.debug_prompt_response import DebugPromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest


class TestDebugPromptResponse(AbstractPromptResponseTest):
    """Test cases for DebugPromptResponse."""

    def get_response_class(self) -> Type[AbstractPromptResponse]:
        return DebugPromptResponse

    def create_test_response(self, text: str, **kwargs) -> AbstractPromptResponse:
        # Remove context from kwargs to avoid passing it twice
        context = kwargs.pop('context', self.context)
        return DebugPromptResponse.create_debug(
            message=text,
            context=context,
            **kwargs
        )

    def get_io_method_name(self) -> str:
        return 'debug'

    def _assert_specific_format(self, rendered: str):
        self.assertIn("🔍", rendered)  # Debug symbol

    def get_expected_lines(self) -> int:
        """Return the expected number of lines in the rendered response."""
        return 1  # Debug messages are single line

    @unittest.skip("Debug messages do not support custom fill characters")
    def test_custom_fill_char(self):
        """Test response with custom fill character."""
        pass

    def test_message_type(self):
        """Test debug message type."""
        response = self.create_test_response(self.test_message)
        self.assertEqual(response.get_message_type(), MessageType.DEBUG)

    def test_multiline_debug(self):
        """Test multiline debug message."""
        message = "Line 1\nLine 2"
        response = self.create_test_response(message)
        rendered = response.render()

        # Check both lines are present
        self.assert_contains_text(rendered, "Line 1")
        self.assert_contains_text(rendered, "Line 2")
