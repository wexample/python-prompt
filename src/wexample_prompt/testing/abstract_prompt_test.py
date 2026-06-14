"""Base class for testing prompt responses."""

from __future__ import annotations

import unittest
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.responses.abstract_prompt_response import (
        AbstractPromptResponse,
    )


class AbstractPromptTest(unittest.TestCase):
    """Base class for testing prompt responses.

    This class provides common functionality for testing prompt responses at three levels:
    1. Response class behavior
    2. IoManager integration
    3. PromptContext implementation
    """

    _io: IoManager
    __test__ = False  # Prevent pytest from discovering this abstract class
    _test_message: str = "Test message"
    _test_message_multiline: str = "Line 1\nLine 2\nLine 3"

    def setUp(self) -> None:
        """Set up common test fixtures."""
        from wexample_prompt.common.io_manager import IoManager

        self._io = IoManager()

    def _assert_contains_text(self, rendered: str, text: str) -> None:
        """Assert that rendered output contains specific text."""
        self.assertIn(text, rendered)

    def _assert_rendered_lines_count(
        self, response: AbstractPromptResponse, lines_count: int
    ) -> None:
        assert response.rendered_content.count("\n") + 1 == lines_count

    def _asset_response_render_is_multiline(
        self, response: AbstractPromptResponse
    ) -> None:
        rendered = response.render()
        self._assert_contains_text(rendered, "Line 1")
        self._assert_contains_text(rendered, "Line 2")
        self._assert_contains_text(rendered, "Line 3")
