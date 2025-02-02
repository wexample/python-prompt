"""Tests for LogPromptResponse."""
from typing import Type

from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.responses.messages.log_prompt_response import LogPromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest


class TestLogPromptResponse(AbstractPromptResponseTest):
    """Test cases for LogPromptResponse."""

    def get_response_class(self) -> Type[AbstractPromptResponse]:
        return LogPromptResponse

    def create_test_response(self, text: str, **kwargs) -> AbstractPromptResponse:
        context = kwargs.pop('context', self.context)
        return LogPromptResponse.create_log(
            message=text,
            context=context,
            **kwargs
        )

    def get_io_method_name(self) -> str:
        return 'log'

    def _assert_specific_format(self, rendered: str):
        # Log messages have no specific format to check
        pass

    def get_expected_lines(self) -> int:
        return 1  # Log messages are single line

    def test_message_type(self):
        response = self.create_test_response(self.test_message)
        self.assertEqual(response.get_message_type(), MessageType.LOG)

    def test_multiline_log(self):
        message = "Line 1\nLine 2"
        response = self.create_test_response(message)
        rendered = response.render()

        self.assert_contains_text(rendered, "Line 1")
        self.assert_contains_text(rendered, "Line 2")

    def test_log_with_timestamp(self):
        timestamp = "2025-01-04 12:00:00"
        message = f"[{timestamp}] System started"

        response = self.create_test_response(message)
        rendered = response.render()

        self.assert_contains_text(rendered, timestamp)
        self.assert_contains_text(rendered, "System started")

    def test_log_with_level(self):
        message = "[INFO] Application initialized"
        response = self.create_test_response(message)
        rendered = response.render()

        self.assert_contains_text(rendered, "[INFO]")
        self.assert_contains_text(rendered, "Application initialized")

    def test_single_indentation(self):
        message = "Indented message"
        response = self.create_test_response(message)
        response.lines[0].indent_level = 1
        rendered = response.render()

        # Should have 2 spaces of indentation
        self.assertTrue(rendered.startswith("  "))
        self.assertEqual("  " + message, rendered)

    def test_multiple_indentation_levels(self):
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

        response = LogPromptResponse(lines=lines, context=self.context)
        rendered = response.render()
        rendered_lines = rendered.split("\n")

        # Check each line has correct indentation
        for i, (indent, msg) in enumerate(messages):
            expected_spaces = "  " * indent
            self.assertTrue(rendered_lines[i].startswith(expected_spaces))
            self.assertTrue(rendered_lines[i].endswith(msg))
