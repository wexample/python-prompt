from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.testing.abstract_prompt_response_test import AbstractPromptResponseTest


class TestEchoPromptResponse(AbstractPromptResponseTest):
    def create_test_response(self, **kwargs) -> AbstractPromptResponse:
        from wexample_prompt.responses.echo_prompt_response import EchoPromptResponse

        kwargs.setdefault("message", self._test_message)
        return EchoPromptResponse.create_echo(**kwargs)

    def _assert_specific_format(self, rendered: str):
        # Echo messages have no specific format to check
        pass

    def get_expected_lines(self) -> int:
        return 1  # Echo messages are single line by default

    def test_empty_response(self):
        """Test empty response."""
        response = self.create_test_response(
            message=""
        )
        self.assertEqual(response.render(), "")

    def test_multiline_response(self):
        """Test multiline response."""
        self._asset_response_render_is_multiline(
            response=self.create_test_response(
                message=self._test_message_multiline
            )
        )
