"""Tests for SubtitlePromptResponse (titles)."""

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.testing.abstract_title_prompt_response_test import AbstractTitlePromptResponseTest


class TestSubtitlePromptResponse(AbstractTitlePromptResponseTest):
    """Focused tests for SubtitlePromptResponse rendering and options."""

    def create_test_response(self, **kwargs) -> AbstractPromptResponse:
        from wexample_prompt.responses.titles.subtitle_prompt_response import (
            SubtitlePromptResponse,
        )
        kwargs.setdefault("text", self._test_message)
        # keep defaults: color=BLUE, character=DEFAULT, width=None
        return SubtitlePromptResponse.create_subtitle(**kwargs)

    def _assert_specific_format(self, rendered: str):
        # Subtitle uses prefix with two spaces then ❯ and default fill char
        self._assert_contains_text(rendered, "  ❯")
        self._assert_contains_text(rendered, "⫻")

    def get_expected_lines(self) -> int:
        # Subtitles render with an empty line before and after
        return 1

    # Keep default common structure from AbstractPromptResponseTest (expects blank lines)

    def test_renders_message_and_format(self):
        response = self.create_test_response()
        rendered = response.render()
        self._assert_common_response_structure(rendered)
        self._assert_contains_text(rendered, self._test_message)
        self._assert_specific_format(rendered)

    def test_custom_character(self):
        response = self.create_test_response(character=".")
        rendered = response.render()
        self._assert_contains_text(rendered, self._test_message)
        self._assert_contains_text(rendered, ".")
        assert "-" not in rendered  # ensure default from legacy not used
