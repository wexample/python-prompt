import unittest
from unittest.mock import patch

from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.common.prompt_context import PromptContext


class AbstractPromptResponseTest(unittest.TestCase):
    """Base class for testing prompt responses.
    
    This class provides common functionality for testing prompt responses at three levels:
    1. Response class behavior
    2. IoManager integration
    3. PromptContext implementation
    """

    def setUp(self):
        """Set up common test fixtures."""
        self.terminal_width = 80
        self.context = PromptContext(terminal_width=self.terminal_width)
        self.io_manager = IoManager(terminal_width=self.terminal_width)

    def assert_common_response_structure(self, rendered: str, expected_lines: int = 3):
        """Assert common structure for rendered responses.
        
        Args:
            rendered: The rendered response string
            expected_lines: Expected number of lines (default 3: empty, content, empty)
        """
        lines = rendered.split("\n")
        self.assertEqual(len(lines), expected_lines)
        
        # First and last lines should be empty
        self.assertEqual(lines[0].strip(), "")
        self.assertEqual(lines[-1].strip(), "")

    def assert_contains_text(self, rendered: str, text: str):
        """Assert that rendered output contains specific text.
        
        Args:
            rendered: The rendered response string
            text: Text to check for
        """
        self.assertIn(text, rendered)

    @patch('wexample_prompt.common.color_manager.ColorManager.supports_color')
    def create_colored_test_context(self, mock_supports_color, color_enabled: bool = True):
        """Create a test context with color support controlled.
        
        Args:
            mock_supports_color: The mocked color support function
            color_enabled: Whether color should be enabled
        
        Returns:
            PromptContext: A context with controlled color support
        """
        mock_supports_color.return_value = color_enabled
        return PromptContext(terminal_width=self.terminal_width)