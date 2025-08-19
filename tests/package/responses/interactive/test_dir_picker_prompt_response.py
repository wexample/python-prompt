"""Tests for DirPickerPromptResponse (interactive)."""

from unittest import mock

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.testing.abstract_prompt_response_test import (
    AbstractPromptResponseTest,
)


class TestDirPickerPromptResponse(AbstractPromptResponseTest):
    """Test cases for DirPickerPromptResponse."""

    def create_test_response(self, **kwargs) -> AbstractPromptResponse:
        from wexample_prompt.responses.interactive.dir_picker_prompt_response import (
            DirPickerPromptResponse,
        )

        # Use a non-existent directory so os.listdir raises and we get a minimal, deterministic layout
        kwargs.setdefault("base_dir", "/nonexistent_dir_for_test")
        kwargs.setdefault("question", self._test_message)
        # keep default abort ("> Abort") behavior unless overridden
        return DirPickerPromptResponse.create_dir_picker(**kwargs)

    def _assert_specific_format(self, rendered: str):
        # Directory picker prompts should have arrow indicators and numbering
        self._assert_contains_text(rendered, "→")
        self._assert_contains_text(rendered, "1.")
        self._assert_contains_text(rendered, "2.")

    def get_expected_lines(self) -> int:
        # Minimal deterministic case: question + parent (..) + "> Select this directory" + abort
        return 4

    # Override: interactive dir picker does not render leading empty line.
    def _assert_common_response_structure(self, rendered: str):
      lines = rendered.split("\n")
      assert len(lines) == self.get_expected_lines()
      # First line should be the question text
      self._assert_contains_text(lines[0], self._test_message)
      # Should list parent and current directory selection label
      self._assert_contains_text(rendered, "..")
      self._assert_contains_text(rendered, "> Select this directory")

    def test_filters_only_directories(self):
        from wexample_prompt.responses.interactive.dir_picker_prompt_response import (
            DirPickerPromptResponse,
        )
        with mock.patch("os.listdir", return_value=["dir1", "file1", "dir2"]), \
             mock.patch("os.path.isdir", side_effect=lambda p: p.endswith(("dir1", "dir2"))):
            response = DirPickerPromptResponse.create_dir_picker(
                base_dir="/tmp/base",
                question=self._test_message,
            )
        rendered = response.render()
        self._assert_contains_text(rendered, "dir1")
        self._assert_contains_text(rendered, "dir2")
        assert "file1" not in rendered

    def test_no_abort_option(self):
        response = self.create_test_response(abort=None)
        rendered = response.render()
        assert "> Abort" not in rendered
        # question + parent + current dir
        non_empty = [l for l in rendered.split("\n") if l.strip()]
        assert len(non_empty) == 3
