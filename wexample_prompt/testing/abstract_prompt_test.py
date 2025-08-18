"""Base class for testing prompt responses."""
import unittest
from abc import ABC

from wexample_prompt.common.io_manager import IoManager


class AbstractPromptTest(unittest.TestCase, ABC):
    """Base class for testing prompt responses.
    
    This class provides common functionality for testing prompt responses at three levels:
    1. Response class behavior
    2. IoManager integration
    3. PromptContext implementation
    """
    _test_message: str = "Test message"
    _io: IoManager

    def setUp(self):
        """Set up common test fixtures."""
        self._io = IoManager()
