"""Tests for ProgressPromptResponse (interactive)."""

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.testing.abstract_prompt_response_test import (
    AbstractPromptResponseTest,
)


class TestProgressPromptResponse(AbstractPromptResponseTest):
    """Focused tests for ProgressPromptResponse core rendering and validation."""

    def create_test_response(self, **kwargs) -> AbstractPromptResponse:
        from wexample_prompt.responses.interactive.progress_prompt_response import (
            ProgressPromptResponse,
        )
        # Sensible defaults
        kwargs.setdefault("total", 10)
        kwargs.setdefault("current", 5)
        kwargs.setdefault("width", 20)
        kwargs.setdefault("label", self._test_message)
        return ProgressPromptResponse.create_progress(**kwargs)

    def _assert_specific_format(self, rendered: str):
        # Should contain percentage and progress characters
        self._assert_contains_text(rendered, "%")
        from wexample_prompt.responses.interactive.progress_prompt_response import (
            ProgressPromptResponse,
        )
        self._assert_contains_text(rendered, ProgressPromptResponse.FILL_CHAR)
        self._assert_contains_text(rendered, ProgressPromptResponse.EMPTY_CHAR)

    def get_expected_lines(self) -> int:
        # Progress bar is single line
        return 1

    # Override: progress does not have leading empty line.
    def _assert_common_response_structure(self, rendered: str):
        lines = rendered.split("\n")
        assert len(lines) == 1
        # Label should be present at start
        self._assert_contains_text(lines[0], self._test_message)
        # Should end with percentage
        assert lines[0].strip().endswith("%")

    def test_create_progress_renders_expected_percentage(self):
        response = self.create_test_response(total=10, current=5, width=20)
        rendered = response.render()
        self._assert_contains_text(rendered, "50%")

    def test_invalid_values_raise(self):
        from wexample_prompt.responses.interactive.progress_prompt_response import (
            ProgressPromptResponse,
        )
        import pytest
        with pytest.raises(ValueError):
            ProgressPromptResponse.create_progress(total=0, current=0)
        with pytest.raises(ValueError):
            ProgressPromptResponse.create_progress(total=10, current=-1)
        with pytest.raises(ValueError):
            ProgressPromptResponse.create_progress(total=10, current=1, width=0)

    def test_custom_style(self):
        from wexample_prompt.responses.interactive.progress_prompt_response import (
            ProgressPromptResponse,
        )
        old_fill = ProgressPromptResponse.FILL_CHAR
        old_empty = ProgressPromptResponse.EMPTY_CHAR
        try:
            ProgressPromptResponse.set_style(fill_char="#", empty_char="-")
            rendered = self.create_test_response().render()
            self._assert_contains_text(rendered, "#")
            self._assert_contains_text(rendered, "-")
        finally:
            ProgressPromptResponse.set_style(fill_char=old_fill, empty_char=old_empty)

    def test_caps_at_100_percent_and_full_bar(self):
        from wexample_prompt.responses.interactive.progress_prompt_response import (
            ProgressPromptResponse,
        )
        resp = self.create_test_response(total=10, current=20, width=10, label=None)
        rendered = resp.render()
        self._assert_contains_text(rendered, "100%")
        # When full, there should be no EMPTY_CHAR present inside the bar segment
        assert ProgressPromptResponse.EMPTY_CHAR not in rendered.split("%")[0]
