"""Tests for TitleResponse."""
import unittest
from unittest.mock import patch

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.titles.title_prompt_response import TitlePromptResponse


class TestTitleResponse(unittest.TestCase):
    """Test cases for TitleResponse."""

    def setUp(self):
        """Set up test cases."""
        self.context = PromptContext(terminal_width=80)
        self.title_text = "Main Title"

    def test_create_title(self):
        """Test creating a title with default settings."""
        title = TitlePromptResponse._create_title(
            text=self.title_text,
            context=self.context,
        )

        rendered = title.render()

        # Check content
        self.assertIn(self.title_text, rendered)
        self.assertIn("❯", rendered)  # Check prefix
        self.assertIn("⫻", rendered)  # Check fill character

        # Check structure
        lines = rendered.split("\n")
        self.assertEqual(len(lines), 3)  # Empty line, title, empty line
        self.assertEqual(lines[0].strip(), "")  # First line empty
        self.assertEqual(lines[2].strip(), "")  # Last line empty

    @patch('wexample_prompt.common.color_manager.ColorManager.supports_color')
    def test_custom_color(self, mock_supports_color):
        """Test title with custom color."""
        mock_supports_color.return_value = True
        title = TitlePromptResponse._create_title(
            text=self.title_text,
            context=self.context,
            color=TerminalColor.RED,
        )
        rendered = title.render()

        # Basic checks
        self.assertIn(self.title_text, rendered)
        self.assertIn("❯", rendered)

        # Color check (basic, as actual color rendering depends on terminal)
        self.assertIn("\033[", rendered)  # ANSI color code start

    def test_custom_fill_char(self):
        """Test title with custom fill character."""
        fill_char = "="
        title = TitlePromptResponse._create_title(
            text=self.title_text,
            context=self.context,
            fill_char=fill_char
        )
        rendered = title.render()

        self.assertIn(self.title_text, rendered)
        self.assertIn(fill_char, rendered)
        self.assertNotIn("⎯", rendered)  # Default fill char should not be present

    def test_no_color(self):
        """Test title without color."""
        title = TitlePromptResponse._create_title(
            text=self.title_text,
            context=self.context,
            color=None
        )
        rendered = title.render()

        self.assertIn(self.title_text, rendered)
        self.assertNotIn("\033[", rendered)  # No ANSI color codes
