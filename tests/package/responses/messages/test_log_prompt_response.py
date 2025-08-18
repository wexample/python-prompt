"""Tests for LogPromptResponse."""
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

