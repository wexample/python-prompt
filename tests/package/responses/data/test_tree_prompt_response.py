"""Tests for TreePromptResponse."""

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.testing.abstract_prompt_response_test import AbstractPromptResponseTest


class TestTreePromptResponse(AbstractPromptResponseTest):
    """Test cases for TreePromptResponse."""

    def create_test_response(self, text: str, **kwargs) -> AbstractPromptResponse:
        from wexample_prompt.responses.data.tree_prompt_response import (
            TreePromptResponse,
        )
        
        data = {
            "root": {
                "folder1": {"file1": "content1", "file2": "content2"},
                "folder2": {"file3": "content3"},
            }
        }
        # Tree response has no title; include the test text as an extra leaf to satisfy base assertion
        data["root"][text] = ""
        return TreePromptResponse.create_tree(
            data=data,
            **kwargs
        )

    def _assert_specific_format(self, rendered: str):
        # Should include tree drawing characters
        self.assertIn("├", rendered)
        self.assertIn("└", rendered)
        self.assertIn("│", rendered)
        self.assertIn("──", rendered)

    def get_expected_lines(self) -> int:
        # Empty lines (1) + root (1) + folder1 (5 files) + folder2 (3 file) + test text (1) + empty (2)
        return 13
