"""Tests for BasePromptResponse."""
import unittest

from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.enums.text_style import TextStyle
from wexample_prompt.enums.response_type import ResponseType
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.responses.base_prompt_response import BasePromptResponse
from wexample_prompt.common.prompt_context import PromptContext


class TestBasePromptResponse(unittest.TestCase):
    """Test cases for BasePromptResponse."""
    
    def test_create_basic_response(self):
        """Test creating a basic text response."""
        line = PromptResponseLine(segments=[
            PromptResponseSegment(text="Hello World")
        ])
        response = BasePromptResponse(
            lines=[line],
            response_type=ResponseType.PLAIN
        )
        self.assertEqual(len(response.lines), 1)
        self.assertEqual(response.response_type, ResponseType.PLAIN)

    def test_response_with_context(self):
        """Test response rendering with context."""
        line = PromptResponseLine(segments=[
            PromptResponseSegment(text="Wide Text")
        ])
        response = BasePromptResponse(
            lines=[line],
            response_type=ResponseType.PLAIN
        )
        context = PromptContext(
            terminal_width=40,
            is_tty=True
        )
        rendered = response.render()
        self.assertLessEqual(len(rendered), 40)

    def test_response_combination(self):
        """Test combining two responses."""
        resp1 = BasePromptResponse(
            lines=[PromptResponseLine(segments=[
                PromptResponseSegment(text="First")
            ])],
            response_type=ResponseType.PLAIN
        )
        resp2 = BasePromptResponse(
            lines=[PromptResponseLine(segments=[
                PromptResponseSegment(text="Second")
            ])],
            response_type=ResponseType.PLAIN
        )
        combined = resp1.append(resp2)
        self.assertEqual(len(combined.lines), 2)

    def test_styled_response(self):
        """Test applying style to entire response."""
        response = BasePromptResponse(
            lines=[PromptResponseLine(segments=[
                PromptResponseSegment(text="Text")
            ])],
            response_type=ResponseType.PLAIN
        )
        styled = response.wrap([TextStyle.BOLD])
        self.assertIn(TextStyle.BOLD, styled.lines[0].segments[0].styles)

    def test_empty_response(self):
        """Test creating an empty response."""
        response = BasePromptResponse(
            lines=[],
            response_type=ResponseType.PLAIN
        )
        self.assertEqual(len(response.lines), 0)
        self.assertEqual(response.render(), "")

    def test_multiline_response(self):
        """Test response with multiple lines."""
        lines = [
            PromptResponseLine(segments=[PromptResponseSegment(text="Line 1")]),
            PromptResponseLine(segments=[PromptResponseSegment(text="Line 2")]),
            PromptResponseLine(segments=[PromptResponseSegment(text="Line 3")])
        ]
        response = BasePromptResponse(
            lines=lines,
            response_type=ResponseType.PLAIN
        )
        rendered = response.render()
        self.assertIn("Line 1", rendered)
        self.assertIn("Line 2", rendered)
        self.assertIn("Line 3", rendered)
