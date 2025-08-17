"""Tests for error handling functionality."""
import io
import unittest

from wexample_prompt.common.io_manager import IoManager


class TestErrorHandling(unittest.TestCase):
    """Test cases for error handling in IoManager."""

    def setUp(self):
        """Set up test cases."""
        self.stdout = io.StringIO()
        self.io = IoManager()
        self.io._stdout = self.stdout

    def tearDown(self):
        """Clean up after tests."""
        self.stdout.close()

    def test_error_basic(self):
        """Test basic error message."""
        self.io.error("Test error")
        output = self.stdout.getvalue()
        self.assertIn("Test error", output)
        self.assertIn("❌", output)  # Error symbol

    def test_error_with_params(self):
        """Test error message with parameters."""
        self.io.error(
            "Error: {code} - {message}",
            params={"code": 404, "message": "Not Found"}
        )
        output = self.stdout.getvalue()
        self.assertIn("Error: 404 - Not Found", output)

    def test_warning_basic(self):
        """Test basic warning message."""
        self.io.warning("Test warning")
        output = self.stdout.getvalue()
        self.assertIn("Test warning", output)
        self.assertIn("⚠️", output)  # Warning symbol

    def test_warning_params(self):
        """Test warning message with parameters."""
        self.io.warning(
            "Warning: {component} is deprecated",
            params={"component": "old_api"}
        )
        output = self.stdout.getvalue()
        self.assertIn("Warning: old_api is deprecated", output)

    def test_error_indentation(self):
        """Test error message with indentation."""
        self.io.log_indent = 2
        self.io.error("Indented error")
        output = self.stdout.getvalue()
        self.assertTrue(any(line.startswith("    ") for line in output.splitlines()))
