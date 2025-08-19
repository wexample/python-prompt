"""Test multiple prompt response."""

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.testing.abstract_prompt_response_test import AbstractPromptResponseTest


class TestMultiplePromptResponse(AbstractPromptResponseTest):
    """Test multiple prompt response."""

    def create_test_response(self, **kwargs) -> AbstractPromptResponse:
        from wexample_prompt.responses.data.multiple_prompt_response import (
            MultiplePromptResponse,
        )
        from wexample_prompt.responses.log_prompt_response import (
            LogPromptResponse,
        )

        message = kwargs.pop("message", self._test_message)
        responses = kwargs.pop("responses", [
            LogPromptResponse.create_log(message=message)
        ])
        return MultiplePromptResponse.create_multiple(
            responses=responses,
            **kwargs
        )

    def _assert_specific_format(self, rendered: str):
        # No specific formatting required for multiple wrapper
        pass

    def get_expected_lines(self) -> int:
        return 1  # Single line aggregation for test message
