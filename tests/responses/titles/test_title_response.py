"""Tests for TitleResponse."""
from typing import Type

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.responses.titles.title_prompt_response import TitlePromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest
from unittest.mock import patch

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.example.example_class_with_context import ExampleClassWithContext


class TestTitleResponse(AbstractPromptResponseTest):
    """Test cases for TitleResponse."""

    def setUp(self):
        super().setUp()
        self.test_message = "Test message"

    def get_response_class(self) -> Type[AbstractPromptResponse]:
        return TitlePromptResponse

    def create_response(self, text: str, **kwargs) -> AbstractPromptResponse:
        return TitlePromptResponse._create_title(
            text=text,
            context=kwargs.get('context', self.context),
            color=kwargs.get('color'),
            fill_char=kwargs.get('fill_char'),
        )

    def get_io_method_name(self) -> str:
        return 'title'

    def _assert_specific_format(self, rendered: str):
        self.assertIn("❯", rendered)  # Check prefix
        self.assertIn("⫻", rendered)  # Check fill character

    def test_response_class(self):
        """Test TitlePromptResponse class behavior."""
        response = self.create_response(self.test_message)

        rendered = response.render()

        # Use common assertions
        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.test_message)

        # specific assertions
        self._assert_specific_format(rendered)

    def test_io_manager(self):
        # Test through IoManager
        title_response = self.io_manager.title(self.test_message)
        rendered = title_response.render()

        # Common structure checks
        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.test_message)

        # Verify it's the right type
        self.assertIsInstance(title_response, TitlePromptResponse)

    def test_prompt_context(self):
        test_context = ExampleClassWithContext(io_manager=self.io_manager)
        response = test_context.title(self.test_message)
        rendered = response.render()

        # Common structure checks
        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.test_message)

        # Context-specific checks
        self.assert_contains_text(rendered, "[EXAMPLE|ExampleClassWithContext]:")  # Should include class prefix
        self.assertIsInstance(response, TitlePromptResponse)

    @patch('wexample_prompt.common.color_manager.ColorManager.supports_color')
    def test_custom_color(self, mock_supports_color):
        context = self.create_colored_test_context(mock_supports_color)

        response = self.create_response(
            self.test_message,
            context=context,
            color=TerminalColor.RED,
        )
        rendered = response.render()

        # Common checks
        self.assert_contains_text(rendered, self.test_message)
        self.assertIn("❯", rendered)

    def test_custom_fill_char(self):
        fill_char = "="
        title = self.create_response(
            self.test_message,
            fill_char=fill_char
        )
        rendered = title.render()

        self.assertIn(self.test_message, rendered)
        self.assertIn(fill_char, rendered)
        self.assertNotIn("⎯", rendered)  # Default fill char should not be present
