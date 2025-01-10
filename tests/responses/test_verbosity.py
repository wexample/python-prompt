"""Test verbosity functionality in prompt responses."""
import unittest
from io import StringIO

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.responses.suggestions_prompt_response import SuggestionsPromptResponse


class TestVerbosity(unittest.TestCase):
    """Test cases for verbosity functionality."""

    def test_verbosity_levels(self):
        """Test that verbosity levels work as expected."""
        # Create contexts with different verbosity levels
        quiet_context = PromptContext(verbosity=VerbosityLevel.QUIET)
        default_context = PromptContext(verbosity=VerbosityLevel.DEFAULT)
        medium_context = PromptContext(verbosity=VerbosityLevel.MEDIUM)
        max_context = PromptContext(verbosity=VerbosityLevel.MAXIMUM)

        # Create responses with different verbosity requirements
        quiet_response = SuggestionsPromptResponse.create(
            message="Critical message",
            suggestions=["critical command"],
            verbosity=VerbosityLevel.QUIET,
            context=quiet_context
        )
        
        normal_response = SuggestionsPromptResponse.create(
            message="Normal message",
            suggestions=["normal command"],
            verbosity=VerbosityLevel.DEFAULT,
            context=default_context
        )
        
        debug_response = SuggestionsPromptResponse.create(
            message="Debug message",
            suggestions=["debug command"],
            verbosity=VerbosityLevel.MAXIMUM,
            context=max_context
        )

        # Test quiet context - should only show QUIET messages
        output = StringIO()
        quiet_response.print(output=output)
        normal_response.print(output=output)
        debug_response.print(output=output)
        quiet_output = output.getvalue()
        self.assertIn("Critical message", quiet_output)
        self.assertNotIn("Normal message", quiet_output)
        self.assertNotIn("Debug message", quiet_output)

        # Test default context - should show QUIET and DEFAULT messages
        output = StringIO()
        quiet_response.print(output=output)
        normal_response.print(output=output)
        debug_response.print(output=output)
        default_output = output.getvalue()
        self.assertIn("Critical message", default_output)
        self.assertIn("Normal message", default_output)
        self.assertNotIn("Debug message", default_output)

        # Test maximum context - should show all messages
        output = StringIO()
        quiet_response.print(output=output)
        normal_response.print(output=output)
        debug_response.print(output=output)
        max_output = output.getvalue()
        self.assertIn("Critical message", max_output)
        self.assertIn("Normal message", max_output)
        self.assertIn("Debug message", max_output)

    def test_should_show_message(self):
        """Test the should_show_message method of PromptContext."""
        context = PromptContext(verbosity=VerbosityLevel.MEDIUM)
        
        # Test all combinations
        self.assertTrue(context.should_show_message(VerbosityLevel.QUIET))
        self.assertTrue(context.should_show_message(VerbosityLevel.DEFAULT))
        self.assertTrue(context.should_show_message(VerbosityLevel.MEDIUM))
        self.assertFalse(context.should_show_message(VerbosityLevel.MAXIMUM))

    def test_empty_output_when_hidden(self):
        """Test that hidden messages produce no output at all."""
        context = PromptContext(verbosity=VerbosityLevel.QUIET)
        response = SuggestionsPromptResponse.create(
            message="Hidden message",
            suggestions=["hidden command"],
            verbosity=VerbosityLevel.MAXIMUM,
            context=context
        )
        
        # Test direct render
        rendered = response.render()
        self.assertEqual(rendered, "")
