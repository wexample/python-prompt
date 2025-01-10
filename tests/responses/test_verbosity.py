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
        critical_response = SuggestionsPromptResponse.create(
            message="Critical message",
            suggestions=["critical command"],
            verbosity=VerbosityLevel.QUIET  # Show even in quiet mode
        )
        
        normal_response = SuggestionsPromptResponse.create(
            message="Normal message",
            suggestions=["normal command"],
            verbosity=VerbosityLevel.DEFAULT  # Show in default and higher
        )
        
        debug_response = SuggestionsPromptResponse.create(
            message="Debug message",
            suggestions=["debug command"],
            verbosity=VerbosityLevel.MAXIMUM  # Only show in maximum verbosity
        )

        def test_context_output(context, expected_messages):
            """Helper to test output in a given context."""
            for response in [critical_response, normal_response, debug_response]:
                response.context = context
            
            output = StringIO()
            critical_response.print(output=output)
            normal_response.print(output=output)
            debug_response.print(output=output)
            result = output.getvalue()
            
            for message, should_appear in expected_messages.items():
                if should_appear:
                    self.assertIn(message, result)
                else:
                    self.assertNotIn(message, result)

        # Test quiet context - should only show critical messages
        test_context_output(quiet_context, {
            "Critical message": True,
            "Normal message": False,
            "Debug message": False
        })

        # Test default context - should show critical and normal messages
        test_context_output(default_context, {
            "Critical message": True,
            "Normal message": True,
            "Debug message": False
        })

        # Test maximum context - should show all messages
        test_context_output(max_context, {
            "Critical message": True,
            "Normal message": True,
            "Debug message": True
        })

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
