"""Tests for file picker responses."""
import os
from typing import Type
from unittest.mock import patch

from wexample_prompt.example.example_class_with_context import ExampleClassWithContext
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.responses.interactive.file_picker_prompt_response import FilePickerPromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest


class TestFilePickerPromptResponse(AbstractPromptResponseTest):
    """Test cases for FilePickerPromptResponse."""

    def setUp(self):
        """Set up test cases."""
        super().setUp()
        self.test_dir = "/test/path"
        self.test_message = "Select a file:"

        # Mock os functions for all tests
        self.patcher_listdir = patch('os.listdir')
        self.patcher_isdir = patch('os.path.isdir')
        self.mock_listdir = self.patcher_listdir.start()
        self.mock_isdir = self.patcher_isdir.start()

        # Set default behavior
        self.mock_listdir.return_value = ["file1.txt"]
        self.mock_isdir.return_value = False

    def tearDown(self):
        """Clean up test cases."""
        super().tearDown()
        self.patcher_listdir.stop()
        self.patcher_isdir.stop()

    def get_response_class(self) -> Type[AbstractPromptResponse]:
        """Get the response class being tested."""
        return FilePickerPromptResponse

    def create_test_response(self, text: str, **kwargs) -> AbstractPromptResponse:
        """Create a test response instance."""
        context = kwargs.pop('context', self.context)
        return FilePickerPromptResponse.create_file_picker(
            base_dir=self.test_dir,
            question=text,
            context=context,
            **kwargs
        )

    def get_io_method_name(self) -> str:
        """Get the name of the IO manager method for this response type."""
        return 'file_picker'

    def _assert_specific_format(self, rendered: str):
        """Assert specific format for file picker responses."""
        # File picker should show arrow indicators and numbering
        self.assert_contains_text(rendered, "→")
        self.assert_contains_text(rendered, "1.")
        self.assert_contains_text(rendered, "2.")

    def get_expected_lines(self) -> int:
        """Get expected number of lines in rendered output."""
        return 3  # Question + file + abort

    def assert_common_response_structure(self, rendered: str):
        """Assert the common structure for file picker responses."""
        lines = rendered.split('\n')
        
        # First line should contain the question
        self.assert_contains_text(lines[0], self.test_message)
        
        # Should have parent directory option
        self.assert_contains_text(rendered, "..")
        
        # Should have abort option
        self.assert_contains_text(rendered, "> Abort")

    def test_create_file_picker(self):
        """Test creating file picker response."""
        # Mock directory listing
        self.mock_listdir.return_value = ["dir1", "file1.txt", "file2.py"]
        self.mock_isdir.side_effect = lambda x: x.endswith("dir1")

        response = self.create_test_response(self.test_message)

        rendered = response.render()
        self.assert_contains_text(rendered, "dir1")
        self.assert_contains_text(rendered, "file1.txt")
        self.assert_contains_text(rendered, "file2.py")
        self.assert_contains_text(rendered, "..")

    def test_execute_select_file(self):
        """Test selecting a file."""
        self.mock_listdir.return_value = ["file1.txt"]
        self.mock_isdir.return_value = False
        expected_path = os.path.join(self.test_dir, "file1.txt")

        with patch('InquirerPy.inquirer.select') as mock_select:
            mock_select.return_value.execute.return_value = "file1.txt"
            
            response = self.create_test_response(self.test_message)
            result = response.execute()
            
            self.assertEqual(result, expected_path)
            mock_select.assert_called_once()

    def test_execute_select_directory(self):
        """Test selecting a directory."""
        # Set up mock behavior for listdir
        dir1_path = os.path.join(self.test_dir, "dir1")
        
        def listdir_side_effect(path):
            if path == self.test_dir:
                return ["dir1"]
            elif path == dir1_path:
                return ["file2.txt"]
            return []
            
        def isdir_side_effect(path):
            return path == dir1_path
        
        self.mock_listdir.side_effect = listdir_side_effect
        self.mock_isdir.side_effect = isdir_side_effect

        with patch('InquirerPy.inquirer.select') as mock_select:
            # First select dir1, then select file2.txt
            mock_select.return_value.execute.side_effect = ["dir1", "file2.txt"]
            
            response = self.create_test_response(self.test_message)
            result = response.execute()
            
            expected_path = os.path.join(self.test_dir, "dir1", "file2.txt")
            self.assertEqual(result, expected_path)
            self.assertEqual(mock_select.call_count, 2)

    def test_execute_abort(self):
        """Test aborting file selection."""
        self.mock_listdir.return_value = ["file1.txt"]
        self.mock_isdir.return_value = False

        with patch('InquirerPy.inquirer.select') as mock_select:
            mock_select.return_value.execute.return_value = None
            
            response = self.create_test_response(self.test_message)
            result = response.execute()
            
            self.assertIsNone(result)
            mock_select.assert_called_once()

    def test_io_manager(self):
        """Test IoManager integration."""
        result = self.io_manager.file_picker(
            base_dir=self.test_dir,
            question=self.test_message
        )
        self.assertIsInstance(result, FilePickerPromptResponse)
