"""Tests for SubtitleResponse."""
from unittest.mock import patch

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.mixins.with_prompt_context import WithPromptContext
from wexample_prompt.responses.titles.subtitle_prompt_response import SubtitlePromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest


class TestSubtitleResponse(AbstractPromptResponseTest):
    """Test cases for SubtitleResponse."""
    
    def setUp(self):
        """Set up test cases."""
        super().setUp()
        self.subtitle_text = "Subtitle Text"
    
    def test_subtitle_response_class(self):
        """Test SubtitlePromptResponse class behavior."""
        subtitle = SubtitlePromptResponse.create_subtitle(
            text=self.subtitle_text,
            context=self.context
        )
        rendered = subtitle.render()
        
        # Use common assertions
        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.subtitle_text)
        
        # Subtitle-specific assertions
        self.assertIn("  ❯", rendered)  # Check prefix with correct indentation
        self.assertIn("⫻", rendered)  # Check default fill character
        
    def test_io_manager_subtitle(self):
        """Test IoManager subtitle() method integration."""
        subtitle_response = self.io_manager.subtitle(self.subtitle_text)
        rendered = subtitle_response.render()
        
        # Common structure checks
        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.subtitle_text)
        
        # Verify it's the right type
        self.assertIsInstance(subtitle_response, SubtitlePromptResponse)
        
    def test_prompt_context_subtitle(self):
        """Test PromptContext implementation of subtitle()."""
        class TestClass(WithPromptContext):
            pass
        
        test_instance = TestClass()
        test_instance.io = self.io_manager
        
        subtitle_response = test_instance.subtitle(self.subtitle_text)
        rendered = subtitle_response.render()
        
        # Common structure checks
        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.subtitle_text)
        
        # Verify it's the right type
        self.assertIsInstance(subtitle_response, SubtitlePromptResponse)
        
    @patch('wexample_prompt.common.color_manager.ColorManager.supports_color')
    def test_custom_color(self, mock_supports_color):
        """Test subtitle with custom color."""
        mock_supports_color.return_value = True
        subtitle = SubtitlePromptResponse.create_subtitle(
            text=self.subtitle_text,
            context=self.context,
            color=TerminalColor.GREEN
        )
        rendered = subtitle.render()
        
        # Common checks
        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.subtitle_text)
        
        # Color check
        self.assertIn("\033[", rendered)  # ANSI color code start
        
    def test_custom_fill_char(self):
        """Test subtitle with custom fill character."""
        fill_char = "."
        subtitle = SubtitlePromptResponse.create_subtitle(
            text=self.subtitle_text,
            context=self.context,
            fill_char=fill_char
        )
        rendered = subtitle.render()
        
        # Common checks
        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.subtitle_text)
        
        # Fill character checks
        self.assertIn(fill_char, rendered)
        self.assertNotIn("-", rendered)  # Default fill char should not be present
