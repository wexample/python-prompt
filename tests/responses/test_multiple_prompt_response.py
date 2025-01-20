"""Tests for MultiplePromptResponse."""
import unittest

from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.enums.response_type import ResponseType
from wexample_prompt.responses.base_prompt_response import BasePromptResponse
from wexample_prompt.responses.multiple_prompt_response import MultiplePromptResponse


class TestMultiplePromptResponse(unittest.TestCase):
    """Test cases for MultiplePromptResponse."""

    def setUp(self):
        """Set up test fixtures."""
        self.base_response1 = BasePromptResponse(
            lines=[PromptResponseLine(segments=[
                PromptResponseSegment(text="First Response")
            ])],
            response_type=ResponseType.PLAIN
        )
        self.base_response2 = BasePromptResponse(
            lines=[PromptResponseLine(segments=[
                PromptResponseSegment(text="Second Response")
            ])],
            response_type=ResponseType.PLAIN
        )

    def test_create_multiple_response(self):
        """Test creating a multiple response."""
        multiple_response = MultiplePromptResponse.create_multiple([
            self.base_response1,
            self.base_response2
        ])

        self.assertEqual(len(multiple_response.responses), 2)
        self.assertEqual(multiple_response.response_type, ResponseType.MULTIPLE)
        self.assertEqual(multiple_response.message_type, MessageType.LOG)

    def test_append_response(self):
        """Test appending a response."""
        multiple_response = MultiplePromptResponse.create_multiple([self.base_response1])
        multiple_response.append_response(self.base_response2)

        self.assertEqual(len(multiple_response.responses), 2)
        self.assertEqual(
            multiple_response.responses[0].lines[0].segments[0].text,
            "First Response"
        )
        self.assertEqual(
            multiple_response.responses[1].lines[0].segments[0].text,
            "Second Response"
        )

    def test_extend_responses(self):
        """Test extending with multiple responses."""
        multiple_response = MultiplePromptResponse.create_multiple([])
        multiple_response.extend_responses([
            self.base_response1,
            self.base_response2
        ])

        self.assertEqual(len(multiple_response.responses), 2)

    def test_render_multiple_responses(self):
        """Test rendering multiple responses."""
        multiple_response = MultiplePromptResponse.create_multiple([
            self.base_response1,
            self.base_response2
        ])

        rendered = multiple_response.render()
        self.assertIn("First Response", rendered)
        self.assertIn("Second Response", rendered)

        self.assertIn("\n", rendered)

    def test_empty_multiple_response(self):
        """Test creating an empty multiple response."""
        multiple_response = MultiplePromptResponse.create_multiple([])

        self.assertEqual(len(multiple_response.responses), 0)
        self.assertEqual(multiple_response.render(), "")
