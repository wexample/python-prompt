"""Tests for EchoPromptResponse."""
from typing import Type

from wexample_prompt.enums.text_style import TextStyle
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.responses.echo_prompt_response import EchoPromptResponse
from wexample_prompt.testing.abstract_prompt_response_test import AbstractPromptResponseTest


class TestEchoPromptResponse(AbstractPromptResponseTest):
    """Test cases for EchoPromptResponse."""

    def get_response_class(self) -> Type[AbstractPromptResponse]:
        return EchoPromptResponse

    def create_test_response(self, text: str, **kwargs) -> AbstractPromptResponse:
        return EchoPromptResponse.create_echo(
            message=text
        )

    def get_io_method_name(self) -> str:
        return 'echo'

    def _assert_specific_format(self, rendered: str):
        # Echo messages have no specific format to check
        pass

    def get_expected_lines(self) -> int:
        return 1  # Echo messages are single line by default

    def test_response_with_style(self):
        """Test response with text styles."""
        response = self.create_test_response(
            "Styled Text",
            styles=[TextStyle.BOLD]
        )
        rendered = response.render()
        self.assert_contains_text(rendered, "Styled Text")

    def test_empty_response(self):
        """Test empty response."""
        response = EchoPromptResponse.create_echo(
            message=""
        )
        self.assertEqual(response.render(), "")

    def test_multiline_response(self):
        """Test multiline response."""
        response = EchoPromptResponse.create_echo(
            message="\n".join(["Line 1", "Line 2", "Line 3"]),
        )
        rendered = response.render()
        self.assert_contains_text(rendered, "Line 1")
        self.assert_contains_text(rendered, "Line 2")
        self.assert_contains_text(rendered, "Line 3")
