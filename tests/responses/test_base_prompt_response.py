"""Tests for BasePromptResponse."""
import unittest
from typing import Type

from wexample_prompt.enums.text_style import TextStyle
from wexample_prompt.enums.response_type import ResponseType
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.responses.base_prompt_response import BasePromptResponse
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.example.abstract_response_example import AbstractResponseExample


class TestBasePromptResponseImpl(BasePromptResponse):
    """Test implementation of BasePromptResponse."""
    
    @classmethod
    def get_example_class(cls) -> Type[AbstractResponseExample]:
        """Get the example class."""
        from wexample_prompt.example.response.messages.log_example import LogExample
        return LogExample

    @classmethod
    def create_test_base_prompt_response_impl(cls, **kwargs) -> 'TestBasePromptResponseImpl':
        """Create a test base prompt response."""
        return cls(**kwargs)


class TestBasePromptResponse(unittest.TestCase):
    """Test cases for BasePromptResponse."""
    
    def test_create_basic_response(self):
        """Test creating a basic text response."""
        line = PromptResponseLine(segments=[
            PromptResponseSegment(text="Hello World")
        ])
        response = TestBasePromptResponseImpl(
            lines=[line],
            response_type=ResponseType.PLAIN,
            context=PromptContext()
        )
        self.assertEqual(len(response.lines), 1)
        self.assertEqual(response.response_type, ResponseType.PLAIN)

    def test_response_with_context(self):
        """Test response rendering with context."""
        line = PromptResponseLine(segments=[
            PromptResponseSegment(text="Wide Text")
        ])
        context = PromptContext(
            terminal_width=40,
            is_tty=True
        )
        response = TestBasePromptResponseImpl(
            lines=[line],
            response_type=ResponseType.PLAIN,
            context=context
        )
        rendered = response.render()
        self.assertLessEqual(len(rendered), 40)

    def test_response_combination(self):
        """Test combining two responses."""
        context = PromptContext()
        resp1 = TestBasePromptResponseImpl(
            lines=[PromptResponseLine(segments=[
                PromptResponseSegment(text="First")
            ])],
            response_type=ResponseType.PLAIN,
            context=context
        )
        resp2 = TestBasePromptResponseImpl(
            lines=[PromptResponseLine(segments=[
                PromptResponseSegment(text="Second")
            ])],
            response_type=ResponseType.PLAIN,
            context=context
        )
        combined = resp1.append(resp2)
        self.assertEqual(len(combined.lines), 2)
        rendered = combined.render()
        self.assertIn("First", rendered)
        self.assertIn("Second", rendered)

    def test_response_with_style(self):
        """Test response with text styles."""
        line = PromptResponseLine(segments=[
            PromptResponseSegment(
                text="Styled Text",
                styles=[TextStyle.BOLD]
            )
        ])
        response = TestBasePromptResponseImpl(
            lines=[line],
            response_type=ResponseType.PLAIN,
            context=PromptContext()
        )
        rendered = response.render()
        self.assertIn("Styled Text", rendered)

    def test_styled_response(self):
        """Test applying style to entire response."""
        response = TestBasePromptResponseImpl(
            lines=[PromptResponseLine(segments=[
                PromptResponseSegment(text="Text")
            ])],
            response_type=ResponseType.PLAIN,
            context=PromptContext()
        )
        styled = response.wrap([TextStyle.BOLD])
        self.assertIn(TextStyle.BOLD, styled.lines[0].segments[0].styles)

    def test_empty_response(self):
        """Test creating an empty response."""
        response = TestBasePromptResponseImpl(
            lines=[],
            response_type=ResponseType.PLAIN,
            context=PromptContext()
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
        response = TestBasePromptResponseImpl(
            lines=lines,
            response_type=ResponseType.PLAIN,
            context=PromptContext()
        )
        rendered = response.render()
        self.assertIn("Line 1", rendered)
        self.assertIn("Line 2", rendered)
        self.assertIn("Line 3", rendered)
