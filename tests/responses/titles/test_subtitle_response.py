from unittest.mock import patch

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.example.example_class_with_context import ExampleClassWithContext
from wexample_prompt.responses.titles.subtitle_prompt_response import SubtitlePromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest


class TestSubtitleResponse(AbstractPromptResponseTest):
    def setUp(self):
        super().setUp()
        self.test_message = "Test message"

    def test_response_class(self):
        """Test SubtitlePromptResponse class behavior."""
        response = SubtitlePromptResponse.create_subtitle(
            text=self.test_message,
            context=self.context,
        )

        rendered = response.render()

        # Use common assertions
        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.test_message)

        # specific assertions
        self.assertIn("  ❯", rendered)  # Check prefix with correct indentation
        self.assertIn("⫻", rendered)  # Check default fill character

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
        response = SubtitlePromptResponse.create_subtitle(
            text=self.test_message,
            context=self.context,
            color=TerminalColor.GREEN
        )
        rendered = response.render()

        # Common checks
        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.test_message)

        # Color check
        self.assertIn("\033[", rendered)

    def test_custom_fill_char(self):
        fill_char = "."
        subtitle = SubtitlePromptResponse.create_subtitle(
            text=self.test_message,
            context=self.context,
            fill_char=fill_char
        )
        rendered = subtitle.render()

        # Common checks
        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.test_message)

        # Fill character checks
        self.assertIn(fill_char, rendered)
        self.assertNotIn("-", rendered)  # Default fill char should not be present
