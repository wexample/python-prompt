"""Tests for BasePromptResponse."""
from typing import Type

from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.enums.text_style import TextStyle
from wexample_prompt.enums.response_type import ResponseType
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.responses.base_prompt_response import BasePromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest


class TestBasePromptResponse(AbstractPromptResponseTest):
    """Test cases for BasePromptResponse."""

    def get_response_class(self) -> Type[AbstractPromptResponse]:
        return BasePromptResponse

    def create_test_response(self, text: str, **kwargs) -> AbstractPromptResponse:
        context = kwargs.pop('context', self.context)
        line = PromptResponseLine(segments=[
            PromptResponseSegment(text=text)
        ])
        return BasePromptResponse.create_base(
            lines=[line],
            context=context,
            **kwargs
        )

    def get_io_method_name(self) -> str:
        return 'base'

    def _assert_specific_format(self, rendered: str):
        # Base messages have no specific format to check
        pass

    def get_expected_lines(self) -> int:
        return 1  # Base messages are single line by default

    def test_response_combination(self):
        """Test combining two responses."""
        resp1 = self.create_test_response("First")
        resp2 = self.create_test_response("Second")
        combined = resp1.append(resp2)
        rendered = combined.render()
        self.assert_contains_text(rendered, "First")
        self.assert_contains_text(rendered, "Second")

    def test_response_with_style(self):
        """Test response with text styles."""
        response = self.create_test_response(
            "Styled Text",
            styles=[TextStyle.BOLD]
        )
        rendered = response.render()
        self.assert_contains_text(rendered, "Styled Text")

    def test_response_type(self):
        """Test response type."""
        response = self.create_test_response(self.test_message)
        self.assertEqual(response.response_type, ResponseType.PLAIN)

    def test_empty_response(self):
        """Test empty response."""
        response = BasePromptResponse.create_base(
            lines=[],
            context=self.context
        )
        self.assertEqual(len(response.lines), 0)
        self.assertEqual(response.render(), "")

    def test_multiline_response(self):
        """Test multiline response."""
        lines = [
            PromptResponseLine(segments=[PromptResponseSegment(text="Line 1")]),
            PromptResponseLine(segments=[PromptResponseSegment(text="Line 2")]),
            PromptResponseLine(segments=[PromptResponseSegment(text="Line 3")])
        ]
        response = BasePromptResponse.create_base(
            lines=lines,
            context=self.context
        )
        rendered = response.render()
        self.assert_contains_text(rendered, "Line 1")
        self.assert_contains_text(rendered, "Line 2")
        self.assert_contains_text(rendered, "Line 3")
