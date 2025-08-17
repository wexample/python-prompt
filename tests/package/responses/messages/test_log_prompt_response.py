"""Tests for LogPromptResponse."""
from typing import Type

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.responses.messages.log_prompt_response import LogPromptResponse
from wexample_prompt.testing.abstract_prompt_response_test import AbstractPromptResponseTest


class TestLogPromptResponse(AbstractPromptResponseTest):
    """Test cases for LogPromptResponse."""

    def get_response_class(self) -> Type[AbstractPromptResponse]:
        return LogPromptResponse

    def create_test_response(self, text: str, **kwargs) -> AbstractPromptResponse:
        return LogPromptResponse.create_log(
            message=text,
            **kwargs
        )

    def test_simple(self):
        response = self.create_test_response(text=self._test_message)
        assert response.render() == self._test_message