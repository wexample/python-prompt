"""Tests for SuggestionsPromptResponse."""
import unittest

from wexample_prompt.responses.suggestions_prompt_response import SuggestionsPromptResponse
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.verbosity_level import VerbosityLevel


class TestSuggestionsPromptResponse(unittest.TestCase):
    """Test cases for SuggestionsPromptResponse."""

    def setUp(self):
        """Set up test cases."""
        self.context = PromptContext(terminal_width=80)
        self.message = "Here is what you can do"
        self.suggestions = [
            "command1 --arg value",
            "command2",
            "command3 --flag"
        ]

    def test_render_with_single_suggestion(self):
        """Test rendering with a single suggestion."""
        response = SuggestionsPromptResponse.create_suggestions(
            message=self.message,
            suggestions=["command1 --arg value"],
            context=self.context
        )
        rendered = response.render()
        self.assertIn(self.message, rendered)
        self.assertIn("command1 --arg value", rendered)
        self.assertIn("→", rendered)  # Check arrow presence

    def test_render_with_multiple_suggestions(self):
        """Test rendering with multiple suggestions."""
        response = SuggestionsPromptResponse.create_suggestions(
            message=self.message,
            suggestions=self.suggestions,
            context=self.context
        )
        rendered = response.render()
        self.assertIn(self.message, rendered)
        for suggestion in self.suggestions:
            self.assertIn(suggestion, rendered)

    def test_render_with_empty_suggestions(self):
        """Test rendering with no suggestions."""
        response = SuggestionsPromptResponse.create_suggestions(
            message=self.message,
            suggestions=[],
            context=self.context
        )
        rendered = response.render()
        self.assertIn(self.message, rendered)
        self.assertNotIn("→", rendered)  # No arrows when no suggestions

    def test_custom_arrow_style(self):
        """Test using a custom arrow style."""
        custom_arrow = ">"
        response = SuggestionsPromptResponse.create_suggestions(
            message=self.message,
            suggestions=self.suggestions,
            arrow_style=custom_arrow,
            context=self.context
        )
        rendered = response.render()
        self.assertIn(custom_arrow, rendered)
        self.assertNotIn("→", rendered)  # Default arrow should not be present

    def test_with_verbosity(self):
        """Test suggestions with verbosity level."""
        # Test with maximum verbosity
        max_context = PromptContext(terminal_width=80, verbosity=VerbosityLevel.MAXIMUM)
        response = SuggestionsPromptResponse.create_suggestions(
            message=self.message,
            suggestions=self.suggestions,
            verbosity=VerbosityLevel.MAXIMUM,
            context=max_context
        )
        rendered = response.render()
        self.assertIn(self.message, rendered)
        for suggestion in self.suggestions:
            self.assertIn(suggestion, rendered)

        # Test with quiet verbosity - should not show anything
        quiet_context = PromptContext(terminal_width=80, verbosity=VerbosityLevel.QUIET)
        response = SuggestionsPromptResponse.create_suggestions(
            message=self.message,
            suggestions=self.suggestions,
            verbosity=VerbosityLevel.MAXIMUM,
            context=quiet_context
        )
        rendered = response.render()
        self.assertEqual("", rendered)
