"""Tests for SuggestionsPromptResponse."""
from typing import Type
from unittest.mock import patch

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.example.example_class_with_context import ExampleClassWithContext
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.responses.data.suggestions_prompt_response import SuggestionsPromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest


class TestSuggestionsPromptResponse(AbstractPromptResponseTest):
    """Test cases for SuggestionsPromptResponse."""

    def setUp(self):
        super().setUp()
        self.message = "Here is what you can do"
        self.suggestions = [
            "command1 --arg value",
            "command2",
            "command3 --flag"
        ]

    def get_response_class(self) -> Type[AbstractPromptResponse]:
        return SuggestionsPromptResponse

    def get_io_method_name(self) -> str:
        return 'suggestions'

    def get_expected_lines(self) -> int:
        return 6  # Empty lines (2) + message line (1) + suggestions (3)

    def _assert_specific_format(self, rendered: str):
        """Assert format specific to suggestions response."""
        lines = rendered.split("\n")
        non_empty_lines = [line for line in lines if line.strip()]
        
        # Should have message line
        self.assertTrue(any(":" in line for line in non_empty_lines))
        
        # Should have arrow indicators
        self.assertTrue(any("→" in line for line in non_empty_lines))

    def create_test_response(self, text: str, **kwargs) -> SuggestionsPromptResponse:
        context = kwargs.pop('context', self.context)
        return SuggestionsPromptResponse.create_suggestions(
            message=text,
            suggestions=self.suggestions,
            context=context,
            **kwargs
        )

    def test_render_with_single_suggestion(self):
        """Test rendering with a single suggestion."""
        response = SuggestionsPromptResponse.create_suggestions(
            message=self.message,
            suggestions=["command1 --arg value"],
            context=self.context
        )
        rendered = response.render()
        self.assert_contains_text(rendered, self.message)
        self.assert_contains_text(rendered, "command1 --arg value")
        self.assert_contains_text(rendered, "→")

    def test_render_with_empty_suggestions(self):
        """Test rendering with no suggestions."""
        response = SuggestionsPromptResponse.create_suggestions(
            message=self.message,
            suggestions=[],
            context=self.context
        )
        rendered = response.render()
        self.assert_contains_text(rendered, self.message)
        self.assertNotIn("→", rendered)

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
        self.assert_contains_text(rendered, custom_arrow)
        self.assertNotIn("→", rendered)

    def test_with_verbosity(self):
        """Test suggestions with verbosity level."""
        # Test with maximum verbosity
        max_context = self.context
        max_context.verbosity = VerbosityLevel.MAXIMUM
        response = SuggestionsPromptResponse.create_suggestions(
            message=self.message,
            suggestions=self.suggestions,
            verbosity=VerbosityLevel.MAXIMUM,
            context=max_context
        )
        rendered = response.render()
        self.assert_contains_text(rendered, self.message)
        for suggestion in self.suggestions:
            self.assert_contains_text(rendered, suggestion)

        # Test with quiet verbosity - should not show anything
        quiet_context = self.context
        quiet_context.verbosity = VerbosityLevel.QUIET
        response = SuggestionsPromptResponse.create_suggestions(
            message=self.message,
            suggestions=self.suggestions,
            verbosity=VerbosityLevel.MAXIMUM,
            context=quiet_context
        )
        rendered = response.render()
        self.assertEqual("", rendered)

    @patch('wexample_prompt.common.color_manager.ColorManager.supports_color')
    def test_custom_color(self, mock_supports_color):
        context = self.create_colored_test_context(mock_supports_color)
        response = self.create_test_response(self.test_message, context=context, color=TerminalColor.GREEN)
        rendered = response.render()
        self.assert_contains_text(rendered, self.test_message)
        self._assert_specific_format(rendered)

    def test_no_color(self):
        response = self.create_test_response(self.message, color=None)
        rendered = response.render()
        self.assert_contains_text(rendered, self.message)
        self._assert_specific_format(rendered)

    def test_io_manager(self):
        """Test IoManager integration."""
        response = self.io_manager.suggestions(
            message=self.message,
            suggestions=self.suggestions
        )
        rendered = response.render()
        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.message)
        self._assert_specific_format(rendered)

    def test_prompt_context(self):
        """Test PromptContext implementation."""
        context = self.context
        class_with_context = ExampleClassWithContext(
            context=context,
            io_manager=self.io_manager
        )
        method = getattr(class_with_context, self.get_io_method_name())
        response = method(
            message=self.message,
            suggestions=self.suggestions
        )
        rendered = response.render()
        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self.message)
        self._assert_specific_format(rendered)
