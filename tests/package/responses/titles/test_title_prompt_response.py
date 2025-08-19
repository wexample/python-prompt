"""Tests for TitlePromptResponse (titles)."""

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.testing.abstract_title_prompt_response_test import AbstractTitlePromptResponseTest


class TestTitlePromptResponse(AbstractTitlePromptResponseTest):
    """Focused tests for TitlePromptResponse rendering and options."""

    def create_test_response(self, **kwargs) -> AbstractPromptResponse:
        from wexample_prompt.responses.titles.title_prompt_response import (
            TitlePromptResponse,
        )
        kwargs.setdefault("text", self._test_message)
        # keep defaults: color=CYAN, character=DEFAULT, width=None
        return TitlePromptResponse.create_title(**kwargs)

    def _assert_specific_format(self, rendered: str):
        # Title uses prefix "❯" and default fill character "⫻"
        self._assert_contains_text(rendered, "❯")
        self._assert_contains_text(rendered, "⫻")

    def get_expected_lines(self) -> int:
        # Titles render with an empty line before and after
        return 1

    # Keep default common structure from AbstractPromptResponseTest (expects blank lines)

    def test_renders_message_and_format(self):
        response = self.create_test_response()
        response.render()
        self._assert_common_response_structure(response)
        self._assert_contains_text(response.rendered_content, self._test_message)
        self._assert_specific_format(response.rendered_content)

    def test_custom_character(self):
        response = self.create_test_response(character="=")
        rendered = response.render()
        self._assert_contains_text(rendered, self._test_message)
        self._assert_contains_text(rendered, "=")
        assert "⫻" not in rendered  # default character should not appear when custom set
