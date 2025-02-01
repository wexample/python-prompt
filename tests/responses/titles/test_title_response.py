"""Tests for TitleResponse."""
from unittest.mock import patch

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.mixins.with_prompt_context import WithPromptContext
from wexample_prompt.responses.titles.title_prompt_response import TitlePromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest


class TestTitleResponse(AbstractPromptResponseTest):
    """Test cases for TitleResponse."""

    def setUp(self):
        """Set up test cases."""
        super().setUp()
        self.title_text = "Main Title"

    def test_title_response_class(self):
        """Test TitlePromptResponse class behavior."""
        title = TitlePromptResponse._create_title(
            text=self.title_text,
            context=self.context,
        )

        rendered = title.render()

        # Use common assertions
        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.title_text)

        # Title-specific assertions
        self.assertIn("❯", rendered)  # Check prefix
        self.assertIn("⫻", rendered)  # Check fill character

    def test_io_manager_title(self):
        """Test IoManager title() method integration."""
        # Test through IoManager
        title_response = self.io_manager.title(self.title_text)
        rendered = title_response.render()

        # Common structure checks
        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.title_text)

        # Verify it's the right type
        self.assertIsInstance(title_response, TitlePromptResponse)

    def test_prompt_context_title(self):
        from pydantic import BaseModel
        """Test PromptContext implementation of title()."""

        # Create a test class with context
        class TestContextClass(WithPromptContext, BaseModel):
            def _format_context_prompt_message(self, message: str, indent: str) -> str:
                return f"{indent}[TEST|{self.__class__.__name__}]: {message}"

        test_context = TestContextClass(io_manager=self.io_manager)
        title_response = test_context.title(self.title_text)
        rendered = title_response.render()

        # Common structure checks
        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.title_text)

        # Context-specific checks
        self.assert_contains_text(rendered, "[TEST|TestContextClass]:")  # Should include class prefix
        self.assertIsInstance(title_response, TitlePromptResponse)

    @patch('wexample_prompt.common.color_manager.ColorManager.supports_color')
    def test_custom_color(self, mock_supports_color):
        """Test title with custom color."""
        context = self.create_colored_test_context(mock_supports_color)

        title = TitlePromptResponse._create_title(
            text=self.title_text,
            context=context,
            color=TerminalColor.RED,
        )
        rendered = title.render()

        # Common checks
        self.assert_contains_text(rendered, self.title_text)
        self.assertIn("❯", rendered)

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
