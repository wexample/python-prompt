"""Tests for directory picker responses."""
import unittest
import os
from unittest.mock import patch

from wexample_prompt.responses.interactive.dir_picker_prompt_response import DirPickerPromptResponse
from wexample_prompt.common.prompt_context import PromptContext


class TestDirPickerPromptResponse(unittest.TestCase):
    """Test cases for DirPickerPromptResponse."""

    def setUp(self):
        """Set up test cases."""
        # Mock terminal size to avoid environment variable issues
        with patch('shutil.get_terminal_size') as mock_term:
            mock_term.return_value.columns = 80
            self.context = PromptContext()
            
        self.test_dir = "/test/path"
        self.question = "Select a directory:"

    @patch('os.listdir')
    @patch('os.path.isdir')
    def test_create_dir_picker(self, mock_isdir, mock_listdir):
        """Test creating directory picker response."""
        # Mock directory listing
        mock_listdir.return_value = ["dir1", "file1", "dir2"]
        mock_isdir.side_effect = lambda x: x.endswith(("dir1", "dir2"))

        response = DirPickerPromptResponse.create_dir_picker(
            base_dir=self.test_dir,
            question=self.question,
            context=self.context
        )

        rendered = response.render()
        self.assertIn(self.question, rendered)
        self.assertIn("📁 dir1", rendered)
        self.assertIn("📁 dir2", rendered)
        self.assertNotIn("file1", rendered)
        self.assertIn("..", rendered)
        self.assertIn("> Select this directory", rendered)

    @patch('os.listdir')
    @patch('os.path.isdir')
    def test_execute_select_current(self, mock_isdir, mock_listdir):
        """Test selecting current directory."""
        mock_listdir.return_value = ["dir1"]
        mock_isdir.return_value = False

        with patch('InquirerPy.inquirer.select') as mock_select:
            mock_select.return_value.execute.return_value = self.test_dir
            
            response = DirPickerPromptResponse.create_dir_picker(
                base_dir=self.test_dir,
                context=self.context
            )
            
            result = response.execute()
            self.assertEqual(result, self.test_dir)

    @patch('os.listdir')
    @patch('os.path.isdir')
    def test_execute_abort(self, mock_isdir, mock_listdir):
        """Test aborting selection."""
        mock_listdir.return_value = ["dir1"]
        mock_isdir.return_value = False

        with patch('InquirerPy.inquirer.select') as mock_select:
            mock_select.return_value.execute.return_value = None
            
            response = DirPickerPromptResponse.create_dir_picker(
                base_dir=self.test_dir,
                context=self.context
            )
            
            result = response.execute()
            self.assertIsNone(result)
