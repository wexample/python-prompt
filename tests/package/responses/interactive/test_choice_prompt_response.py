"""Tests for ChoicePromptResponse (interactive)."""

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
        kwargs.setdefault("predefined_answer", "Option 2")
        # keep default abort ("> Abort") behavior unless overridden
        return ChoicePromptResponse.create_choice(**kwargs)

    def _assert_specific_format(self, rendered: str):
        # Choice prompts should have arrow indicators and numbering
        self._assert_contains_text(rendered, "›")
        self._assert_contains_text(rendered, "⨯")

    def get_expected_lines(self) -> int:
        # By default: question (1) + 2 choices + abort (1)
        return 6

    # Override: interactive choice does not render leading empty line.
    def _assert_common_response_structure(self, response: "AbstractPromptResponse"):
        lines = response.rendered_content.split("\n")
        assert len(lines) == self.get_expected_lines()
        # First line should be the question text
        self._assert_contains_text(lines[0], self._test_message)
        # Each choice line should be properly formatted
        for i, choice in enumerate(["Option 1", "Option 2"], start=1):
            choice_line = lines[i]
            self._assert_contains_text(choice_line, choice)

    def test_create_with_choice_objects(self):
        from wexample_prompt.responses.interactive.choice_prompt_response import (
            ChoicePromptResponse,
        )
        choices = {
            "value1": "Display 1",
            "value2": "Display 2",
        }

        response = ChoicePromptResponse.create_choice(
            question=self._test_message,
            choices=choices,
            predefined_answer="value2",
        )

        response.render()

        self._assert_contains_text(response.rendered_content, "Display 1")
        self._assert_contains_text(response.rendered_content, "Display 2")
        assert "value1" not in response.rendered_content
        assert "value2" not in response.rendered_content

    def test_abort_option(self):
        abort_text = "Cancel"
        response = self.create_test_response(abort=abort_text)
        response.render()
        self._assert_contains_text(response.rendered_content, abort_text)
        # abort should be numbered after the choices
        self._assert_contains_text(response.rendered_content, str(len(["Option 1", "Option 2"]) + 1))

    def test_no_abort_option(self):
        response = self.create_test_response(abort=None)
        response.render()

        assert "> Abort" not in response.rendered_content
        # question + 2 choices
        non_empty = [l for l in response.rendered_content.split("\n") if l.strip()]
        assert len(non_empty) == 6
