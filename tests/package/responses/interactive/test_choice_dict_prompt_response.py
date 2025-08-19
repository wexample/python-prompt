"""Tests for ChoiceDictPromptResponse (interactive)."""

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.testing.abstract_prompt_response_test import (
    AbstractPromptResponseTest,
)


class TestChoiceDictPromptResponse(AbstractPromptResponseTest):
    """Test cases for ChoiceDictPromptResponse."""

    def create_test_response(self, **kwargs) -> AbstractPromptResponse:
        from wexample_prompt.responses.interactive.choice_dict_prompt_response import (
            ChoiceDictPromptResponse,
        )

        kwargs.setdefault("question", self._test_message)
        kwargs.setdefault("choices", {"key1": "Value 1", "key2": "Value 2"})
        # keep default abort ("> Abort") behavior unless overridden
        return ChoiceDictPromptResponse.create_choice_dict(**kwargs)

    def _assert_specific_format(self, rendered: str):
        # Choice dict prompts should have arrow indicators and numbering
        self._assert_contains_text(rendered, "→")
        self._assert_contains_text(rendered, "1.")
        self._assert_contains_text(rendered, "2.")

    def get_expected_lines(self) -> int:
        # By default: question (1) + 2 choices + abort (1)
        return 4

    # Override: interactive choice does not render leading empty line.
    def _assert_common_response_structure(self, rendered: str):
        lines = rendered.split("\n")
        assert len(lines) == self.get_expected_lines()
        # First line should be the question text
        self._assert_contains_text(lines[0], self._test_message)
        # Each choice line should be properly formatted (values visible, keys hidden)
        expected_values = ["Value 1", "Value 2"]
        expected_keys = ["key1", "key2"]
        for i, value in enumerate(expected_values, start=1):
            choice_line = lines[i]
            self._assert_contains_text(choice_line, f"{i}.")
            self._assert_contains_text(choice_line, "→")
            self._assert_contains_text(choice_line, value)
            for k in expected_keys:
                assert k not in choice_line

    def test_create_with_dict(self):
        response = self.create_test_response()
        rendered = response.render()
        self._assert_contains_text(rendered, "Value 1")
        self._assert_contains_text(rendered, "Value 2")
        assert "key1" not in rendered
        assert "key2" not in rendered

    def test_abort_option(self):
        abort_text = "Cancel"
        response = self.create_test_response(abort=abort_text)
        rendered = response.render()
        self._assert_contains_text(rendered, abort_text)
        # abort should be numbered after the choices
        self._assert_contains_text(rendered, str(2 + 1))

    def test_no_abort_option(self):
        response = self.create_test_response(abort=None)
        rendered = response.render()
        assert "> Abort" not in rendered
        # question + 2 choices
        non_empty = [l for l in rendered.split("\n") if l.strip()]
        assert len(non_empty) == 3
