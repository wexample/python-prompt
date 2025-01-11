"""Tests for SubtitleResponse."""
import unittest
from unittest.mock import patch

from wexample_prompt.responses.titles.subtitle_response import SubtitleResponse
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.terminal_color import TerminalColor


class TestSubtitleResponse(unittest.TestCase):
    """Test cases for SubtitleResponse."""
    
    def setUp(self):
        """Set up test cases."""
        self.context = PromptContext(terminal_width=80)
        self.subtitle_text = "Subtitle Text"
    
    def test_create_subtitle(self):
        """Test creating a subtitle with default settings."""
        subtitle = SubtitleResponse.create_subtitle(text=self.subtitle_text)
        rendered = subtitle.render()
        
        # Check content
        self.assertIn(self.subtitle_text, rendered)
        self.assertIn("  ▷", rendered)  # Check prefix with correct indentation
        self.assertIn("-", rendered)  # Check default fill character
        
        # Check structure
        lines = rendered.split("\n")
        self.assertEqual(len(lines), 3)  # Empty line, subtitle, empty line
        self.assertEqual(lines[0].strip(), "")  # First line empty
        self.assertEqual(lines[2].strip(), "")  # Last line empty
        
    @patch('wexample_prompt.common.color_manager.ColorManager.supports_color')
    def test_custom_color(self, mock_supports_color):
        """Test subtitle with custom color."""
        mock_supports_color.return_value = True
        subtitle = SubtitleResponse.create_subtitle(
            text=self.subtitle_text,
            color=TerminalColor.GREEN
        )
        rendered = subtitle.render()
        
        # Basic checks
        self.assertIn(self.subtitle_text, rendered)
        self.assertIn("  ▷", rendered)
        
        # Color check (basic, as actual color rendering depends on terminal)
        self.assertIn("\033[", rendered)  # ANSI color code start
        
    def test_custom_fill_char(self):
        """Test subtitle with custom fill character."""
        fill_char = "."
        subtitle = SubtitleResponse.create_subtitle(
            text=self.subtitle_text,
            fill_char=fill_char
        )
        rendered = subtitle.render()
        
        self.assertIn(self.subtitle_text, rendered)
        self.assertIn(fill_char, rendered)
        self.assertNotIn("-", rendered)  # Default fill char should not be present
        
    def test_no_color(self):
        """Test subtitle without color."""
        subtitle = SubtitleResponse.create_subtitle(
            text=self.subtitle_text,
            color=None
        )
        rendered = subtitle.render()
        
        self.assertIn(self.subtitle_text, rendered)
        self.assertNotIn("\033[", rendered)  # No ANSI color codes
        
    def test_indentation_consistency(self):
        """Test that subtitle prefix maintains correct indentation."""
        subtitle = SubtitleResponse.create_subtitle(text=self.subtitle_text)
        rendered = subtitle.render()
        
        # The prefix should start with exactly two spaces
        lines = rendered.split("\n")
        title_line = lines[1]  # The middle line contains the actual subtitle
        self.assertTrue(title_line.startswith("  ▷"), "Subtitle should start with two spaces and arrow")
