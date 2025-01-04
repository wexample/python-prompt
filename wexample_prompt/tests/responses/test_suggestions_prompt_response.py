import unittest

from wexample_prompt.responses.suggestions_prompt_response import SuggestionsPromptResponse


class TestSuggestionsPromptResponse(unittest.TestCase):
    """Test cases for SuggestionsPromptResponse."""

    def test_render_with_single_suggestion(self):
        """Test rendering with a single suggestion."""
        response = SuggestionsPromptResponse.create(
            message="Here is what you can do",
            suggestions=["command1 --arg value"]
        )
        self.assertEqual(len(response.lines), 2)
        self.assertIn("Here is what you can do:", response.lines[0].render())
        self.assertIn("command1 --arg value", response.lines[1].render())

    def test_render_with_multiple_suggestions(self):
        """Test rendering with multiple suggestions."""
        response = SuggestionsPromptResponse.create(
            message="Choose one of these commands",
            suggestions=[
                "command1 --arg value",
                "command2",
                "command3 --flag"
            ]
        )
        self.assertEqual(len(response.lines), 4)
        self.assertIn("Choose one of these commands:", response.lines[0].render())
        self.assertIn("command1 --arg value", response.lines[1].render())
        self.assertIn("command2", response.lines[2].render())
        self.assertIn("command3 --flag", response.lines[3].render())

    def test_render_with_empty_suggestions(self):
        """Test rendering with no suggestions."""
        response = SuggestionsPromptResponse.create(
            message="No actions available",
            suggestions=[]
        )
        self.assertEqual(len(response.lines), 1)
        self.assertIn("No actions available:", response.lines[0].render())
