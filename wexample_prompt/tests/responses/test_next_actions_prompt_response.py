import unittest

from wexample_prompt.responses.next_actions_prompt_response import NextActionsPromptResponse


class TestNextActionsPromptResponse(unittest.TestCase):
    """Test cases for NextActionsPromptResponse."""

    def test_render_with_single_suggestion(self):
        """Test rendering with a single suggestion."""
        response = NextActionsPromptResponse.create(
            message="Here is what you can do",
            suggestions=["command1 --arg value"]
        )
        self.assertEqual(len(response.lines), 2)
        self.assertEqual(response.lines[0].render(), "Here is what you can do:")
        self.assertEqual(response.lines[1].render(), "  • command1 --arg value")

    def test_render_with_multiple_suggestions(self):
        """Test rendering with multiple suggestions."""
        response = NextActionsPromptResponse.create(
            message="Choose one of these commands",
            suggestions=[
                "command1 --arg value",
                "command2",
                "command3 --flag"
            ]
        )
        self.assertEqual(len(response.lines), 4)
        self.assertEqual(response.lines[0].render(), "Choose one of these commands:")
        self.assertEqual(response.lines[1].render(), "  • command1 --arg value")
        self.assertEqual(response.lines[2].render(), "  • command2")
        self.assertEqual(response.lines[3].render(), "  • command3 --flag")

    def test_render_with_empty_suggestions(self):
        """Test rendering with no suggestions."""
        response = NextActionsPromptResponse.create(
            message="No actions available",
            suggestions=[]
        )
        self.assertEqual(len(response.lines), 1)
        self.assertEqual(response.lines[0].render(), "No actions available:")
