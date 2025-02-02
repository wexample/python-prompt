"""Tests for file picker responses."""
import os
from unittest.mock import patch

from wexample_prompt.responses.interactive.file_picker_prompt_response import FilePickerPromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest


class TestFilePickerPromptResponse(AbstractPromptResponseTest):
    """Test cases for FilePickerPromptResponse."""

    def setUp(self):
        """Set up test cases."""
        # Mock terminal size to avoid environment variable issues
        with patch('shutil.get_terminal_size') as mock_term:
            mock_term.return_value.columns = 80
            super().setUp()

        self.test_dir = "/test/path"
        self.question = "Select a file:"

    @patch('os.listdir')
    @patch('os.path.isdir')
    def test_create_file_picker(self, mock_isdir, mock_listdir):
        """Test creating file picker response."""
        # Mock directory listing
        mock_listdir.return_value = ["dir1", "file1.txt", "file2.py"]
        mock_isdir.side_effect = lambda x: x.endswith("dir1")

        response = FilePickerPromptResponse.create_file_picker(
            base_dir=self.test_dir,
            question=self.question,
            context=self.context
        )

        rendered = response.render()
        self.assertIn(self.question, rendered)
        self.assertIn("📁 dir1", rendered)
        self.assertIn("file1.txt", rendered)
        self.assertIn("file2.py", rendered)
        self.assertIn("..", rendered)

    @patch('os.listdir')
    @patch('os.path.isdir')
    def test_execute_select_file(self, mock_isdir, mock_listdir):
        """Test selecting a file."""
        mock_listdir.return_value = ["file1.txt"]
        mock_isdir.return_value = False
        expected_path = os.path.join(self.test_dir, "file1.txt")

        with patch('InquirerPy.inquirer.select') as mock_select:
            mock_select.return_value.execute.return_value = "file1.txt"

            response = FilePickerPromptResponse.create_file_picker(
                base_dir=self.test_dir,
                context=self.context
            )

            result = response.execute()
            self.assertEqual(result, expected_path)

    @patch('os.listdir')
    @patch('os.path.isdir')
    def test_execute_abort(self, mock_isdir, mock_listdir):
        """Test aborting the selection."""
        mock_listdir.return_value = ["file1.txt"]
        mock_isdir.return_value = False

        with patch('InquirerPy.inquirer.select') as mock_select:
            mock_select.return_value.execute.return_value = None

            response = FilePickerPromptResponse.create_file_picker(
                base_dir=self.test_dir,
                context=self.context
            )

            result = response.execute()
            self.assertIsNone(result)
