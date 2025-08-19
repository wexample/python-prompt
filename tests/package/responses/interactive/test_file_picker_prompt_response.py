"""Tests for FilePickerPromptResponse (interactive)."""

from unittest import mock

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.testing.abstract_prompt_response_test import (
    AbstractPromptResponseTest,
)


class TestFilePickerPromptResponse(AbstractPromptResponseTest):
    """Test cases for FilePickerPromptResponse."""

    def create_test_response(self, **kwargs) -> AbstractPromptResponse:
        from wexample_prompt.responses.interactive.file_picker_prompt_response import (
            FilePickerPromptResponse,
        )

        # Deterministic minimal case when listing fails
        kwargs.setdefault("base_dir", "/nonexistent_dir_for_test")
        kwargs.setdefault("question", self._test_message)
        # keep default abort ("> Abort") unless overridden
        return FilePickerPromptResponse.create_file_picker(**kwargs)

    def _assert_specific_format(self, rendered: str):
        # File picker prompts should have arrow indicators and numbering
        self._assert_contains_text(rendered, "→")
        self._assert_contains_text(rendered, "1.")
        self._assert_contains_text(rendered, "2.")

    def get_expected_lines(self) -> int:
        # Minimal default: question + parent (..) + (no files/dirs due to failure) + abort
        # But render builds from merged dict (at least parent), plus abort.
        return 3  # question + parent + abort

    # Override: interactive file picker does not render leading empty line.
    def _assert_common_response_structure(self, rendered: str):
        lines = rendered.split("\n")
        assert len(lines) == self.get_expected_lines()
        # First line should be the question text
        self._assert_contains_text(lines[0], self._test_message)
        # Should list parent
        self._assert_contains_text(rendered, "..")

    def test_lists_dirs_and_files_separately_then_merges(self):
        from wexample_prompt.responses.interactive.file_picker_prompt_response import (
            FilePickerPromptResponse,
        )
        with mock.patch("os.listdir", return_value=["dir1", "file1", "dir2", "file2"]), \
             mock.patch("os.path.isdir", side_effect=lambda p: p.endswith(("dir1", "dir2"))):
            response = FilePickerPromptResponse.create_file_picker(
                base_dir="/tmp/base",
                question=self._test_message,
            )
        rendered = response.render()
        # dirs should be present (with a leading space label per implementation)
        self._assert_contains_text(rendered, " dir1")
        self._assert_contains_text(rendered, " dir2")
        # files should be present with their names
        self._assert_contains_text(rendered, "file1")
        self._assert_contains_text(rendered, "file2")

    def test_no_abort_option(self):
        response = self.create_test_response(abort=None)
        rendered = response.render()
        assert "> Abort" not in rendered
        # question + parent only in the minimal fallback
        non_empty = [l for l in rendered.split("\n") if l.strip()]
        assert len(non_empty) == 2
