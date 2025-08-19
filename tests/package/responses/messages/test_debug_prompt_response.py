from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.testing.abstract_prompt_response_test import AbstractPromptResponseTest


class TestDebugPromptResponse(AbstractPromptResponseTest):
    def create_test_response(self, **kwargs) -> AbstractPromptResponse:
        from wexample_prompt.responses.messages.debug_prompt_response import DebugPromptResponse

        kwargs.setdefault("message", self._test_message)
        return DebugPromptResponse.create_debug(**kwargs)

    def _assert_specific_format(self, rendered: str):
        # Debug messages should include the debug symbol
        self._assert_contains_text(rendered, "🔍")

    def get_expected_lines(self) -> int:
        return 1  # Debug messages are single line

    def test_multiline_response(self):
        """Test multiline response."""
        self._asset_response_render_is_multiline(
            response=self.create_test_response(
                message=self._test_message_multiline
            )
        )

