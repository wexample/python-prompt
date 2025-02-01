"""Tests for SubtitleResponse."""
from typing import Type, TYPE_CHECKING
from unittest.mock import patch

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.example.example_class_with_context import ExampleClassWithContext
from wexample_prompt.responses.titles.subtitle_prompt_response import SubtitlePromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest

if TYPE_CHECKING:
    from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse

class TestSubtitleResponse(AbstractPromptResponseTest):
    """Test cases for SubtitleResponse."""

    def setUp(self):
        super().setUp()
        self.test_message = "Test message"

    def get_response_class(self) -> Type["AbstractPromptResponse"]:
        return SubtitlePromptResponse

    def create_response(self, text: str, **kwargs) -> "AbstractPromptResponse":
        return SubtitlePromptResponse.create_subtitle(
            text=text,
            context=kwargs.get('context', self.context),
            color=kwargs.get('color'),
            fill_char=kwargs.get('fill_char'),
        )

    def get_io_method_name(self) -> str:
        return 'subtitle'

    def _assert_specific_format(self, rendered: str):
        self.assertIn("  ❯", rendered)  # Check prefix with correct indentation
        self.assertIn("⫻", rendered)  # Check fill character

    def test_response_class(self):
        """Test SubtitlePromptResponse class behavior."""
        response = self.create_response(self.test_message)

        rendered = response.render()

        # Use common assertions
        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.test_message)

        # specific assertions
        self._assert_specific_format(rendered)

    def test_io_manager(self):
        response = self.io_manager.subtitle(self.test_message)
        rendered = response.render()

        # Common structure checks
        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.test_message)

        # Verify it's the right type
        self.assertIsInstance(response, SubtitlePromptResponse)

    def test_prompt_context(self):
        test_context = ExampleClassWithContext(io_manager=self.io_manager)
        response = test_context.subtitle(self.test_message)
        rendered = response.render()

        # Common structure checks
        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.test_message)

        # Verify it's the right type
        self.assertIsInstance(response, SubtitlePromptResponse)

    @patch('wexample_prompt.common.color_manager.ColorManager.supports_color')
    def test_custom_color(self, mock_supports_color):
        mock_supports_color.return_value = True
        response = self.create_response(self.test_message, color=TerminalColor.GREEN)
        rendered = response.render()

        # Common checks
        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.test_message)

        # Color check
        self.assertIn("\033[", rendered)

    def test_custom_fill_char(self):
        fill_char = "."
        subtitle = self.create_response(self.test_message, fill_char=fill_char)
        rendered = subtitle.render()

        # Common checks
        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.test_message)

        # Fill character checks
        self.assertIn(fill_char, rendered)
        self.assertNotIn("-", rendered)  # Default fill char should not be present
