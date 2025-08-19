"""Tests for LogPromptResponse."""
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.testing.abstract_prompt_response_test import AbstractPromptResponseTest


class TestLogPromptResponse(AbstractPromptResponseTest):
    """Test cases for LogPromptResponse."""

    def create_test_response(self, text: str, **kwargs) -> AbstractPromptResponse:
        from wexample_prompt.responses.log_prompt_response import LogPromptResponse

        return LogPromptResponse.create_log(
            message=text,
            **kwargs
        )

    def _assert_specific_format(self, rendered: str):
        # Log messages have no specific format to check
        pass

    def get_expected_lines(self) -> int:
        return 1  # Log messages are single line

    def test_multiline_log(self):
        message = "Line 1\nLine 2"
        response = self.create_test_response(message)
        rendered = response.render()

        self._assert_contains_text(rendered, "Line 1")
        self._assert_contains_text(rendered, "Line 2")

    def test_log_with_timestamp(self):
        timestamp = "2025-01-04 12:00:00"
        message = f"[{timestamp}] System started"

        response = self.create_test_response(message)
        rendered = response.render()

        self._assert_contains_text(rendered, timestamp)
        self._assert_contains_text(rendered, "System started")

    def test_log_with_level(self):
        message = "[INFO] Application initialized"
        response = self.create_test_response(message)
        rendered = response.render()

        self._assert_contains_text(rendered, "[INFO]")
        self._assert_contains_text(rendered, "Application initialized")

    def test_single_indentation(self):
        message = "Indented message"
        response = self.create_test_response(message)
        rendered = response.render(
            context=PromptContext(
                indentation=2
            )
        )

        # Should have 2 spaces of indentation
        assert rendered.startswith("  ")

    def test_multiple_indentation_levels(self):
        messages = [
            (0, "Root level"),
            (1, "First indent"),
            (2, "Second indent"),
            (3, "Third indent"),
            (1, "Back to first"),
        ]

        # Create response with multiple lines at different indentation levels
        for indent, message in messages:
            response = self.create_test_response(message)
            rendered = response.render(
                context=PromptContext(
                    indentation=indent
                )
            )
            assert rendered.startswith("  " * indent)
