"""Tests for ChoicePromptResponse (interactive)."""

from InquirerPy.base.control import Choice

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.testing.abstract_prompt_response_test import (
    AbstractPromptResponseTest,
)


class TestChoicePromptResponse(AbstractPromptResponseTest):
    """Test cases for ChoicePromptResponse."""

    def create_test_response(self, **kwargs) -> AbstractPromptResponse:
        from wexample_prompt.responses.interactive.choice_prompt_response import (
            ChoicePromptResponse,
        )

        kwargs.setdefault("question", self._test_message)
        kwargs.setdefault("choices", ["Option 1", "Option 2"])
        # keep default abort ("> Abort") behavior unless overridden
        return ChoicePromptResponse.create_choice(**kwargs)

    def _assert_specific_format(self, rendered: str):
        # Choice prompts should have arrow indicators and numbering
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
        # Each choice line should be properly formatted
        for i, choice in enumerate(["Option 1", "Option 2"], start=1):
            choice_line = lines[i]
            self._assert_contains_text(choice_line, f"{i}.")
            self._assert_contains_text(choice_line, "→")
            self._assert_contains_text(choice_line, choice)

    def test_create_with_choice_objects(self):
        from wexample_prompt.responses.interactive.choice_prompt_response import (
            ChoicePromptResponse,
        )
        choices = [Choice("value1", "Display 1"), Choice("value2", "Display 2")]
        response = ChoicePromptResponse.create_choice(
            question=self._test_message,
            choices=choices,
        )
        rendered = response.render()
        self._assert_contains_text(rendered, "Display 1")
        self._assert_contains_text(rendered, "Display 2")
        assert "value1" not in rendered
        assert "value2" not in rendered

    def test_abort_option(self):
        abort_text = "Cancel"
        response = self.create_test_response(abort=abort_text)
        rendered = response.render()
        self._assert_contains_text(rendered, abort_text)
        # abort should be numbered after the choices
        self._assert_contains_text(rendered, str(len(["Option 1", "Option 2"]) + 1))

    def test_no_abort_option(self):
        response = self.create_test_response(abort=None)
        rendered = response.render()
        assert "> Abort" not in rendered
        # question + 2 choices
        non_empty = [l for l in rendered.split("\n") if l.strip()]
        assert len(non_empty) == 3
