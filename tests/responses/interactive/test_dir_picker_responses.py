"""Tests for directory picker responses."""
from typing import Type
from unittest.mock import patch

from wexample_prompt.example.example_class_with_context import ExampleClassWithContext
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.responses.interactive.dir_picker_prompt_response import DirPickerPromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest


class TestDirPickerPromptResponse(AbstractPromptResponseTest):
    """Test cases for DirPickerPromptResponse."""

    def setUp(self):
        """Set up test cases."""
        super().setUp()
        self.test_dir = "/test/path"
        self.question = "Select a directory:"

        # Mock os functions for all tests
        self.patcher_listdir = patch('os.listdir')
        self.patcher_isdir = patch('os.path.isdir')
        self.mock_listdir = self.patcher_listdir.start()
        self.mock_isdir = self.patcher_isdir.start()

        # Set default behavior
        self.mock_listdir.return_value = ["dir1"]
        self.mock_isdir.return_value = False

    def tearDown(self):
        """Clean up test cases."""
        super().tearDown()
        self.patcher_listdir.stop()
        self.patcher_isdir.stop()

    def get_response_class(self) -> Type[AbstractPromptResponse]:
        return DirPickerPromptResponse

    def create_test_response(self, text: str, **kwargs) -> AbstractPromptResponse:
        context = kwargs.pop('context', self.context)
        return DirPickerPromptResponse.create_dir_picker(
            question=text,
            base_dir=self.test_dir,
            context=context,
            **kwargs
        )

    def get_io_method_name(self) -> str:
        return 'dir_picker'

    def _assert_specific_format(self, rendered: str):
        # Directory picker prompts should have arrow indicators and numbering
        self.assert_contains_text(rendered, "→")
        self.assert_contains_text(rendered, "1.")
        self.assert_contains_text(rendered, "2.")

    def get_expected_lines(self) -> int:
        return 4  # Question + parent dir + current dir + abort

    def assert_common_response_structure(self, rendered: str):
        """Assert the common structure for directory picker responses.
        
        Overrides the parent method since directory picker responses have a different structure.
        """
        lines = rendered.split('\n')

        # First line should contain the question
        self.assert_contains_text(lines[0], self.test_message)

        # Should have the correct number of lines
        self.assertEqual(len([l for l in lines if l.strip()]), self.get_expected_lines())

        # Should have parent directory option
        self.assert_contains_text(rendered, "..")

        # Should have current directory option
        self.assert_contains_text(rendered, "> Select this directory")

    def test_create_dir_picker(self):
        """Test creating directory picker response."""
        # Mock directory listing
        self.mock_listdir.return_value = ["dir1", "file1", "dir2"]
        self.mock_isdir.side_effect = lambda x: x.endswith(("dir1", "dir2"))

        response = self.create_test_response(self.test_message)

        rendered = response.render()
        self.assert_contains_text(rendered, "dir1")
        self.assert_contains_text(rendered, "dir2")
        self.assertNotIn("file1", rendered)

    @patch('InquirerPy.inquirer.select')
    def test_execute_select_current(self, mock_select):
        """Test selecting current directory."""
        mock_select.return_value.execute.return_value = self.test_dir

        response = self.create_test_response(self.test_message)
        result = response.execute()

        self.assertEqual(result, self.test_dir)
        mock_select.assert_called_once()

    @patch('InquirerPy.inquirer.select')
    def test_execute_abort(self, mock_select):
        """Test aborting selection."""
        mock_select.return_value.execute.return_value = None

        response = self.create_test_response(self.test_message)
        result = response.execute()

        self.assertIsNone(result)
        mock_select.assert_called_once()

    @patch('InquirerPy.inquirer.select')
    def test_io_manager(self, mock_select):
        """Test IoManager integration."""
        method = getattr(self.io, self.get_io_method_name())
        result = method(self.test_message, base_dir=self.test_dir)

        # Verify that we get a DirPickerPromptResponse object
        self.assertIsInstance(result, DirPickerPromptResponse)
        mock_select.assert_not_called()  # select ne devrait pas être appelé car on n'appelle pas execute()

    @patch('InquirerPy.inquirer.select')
    def test_prompt_context(self, mock_select):
        """Test PromptContext implementation."""
        context = self.context
        class_with_context = ExampleClassWithContext(
            context=context,
            io=self.io
        )
        method = getattr(class_with_context, self.get_io_method_name())
        result = method(self.test_message, base_dir=self.test_dir)

        # Verify that we get a DirPickerPromptResponse object
        self.assertIsInstance(result, DirPickerPromptResponse)
        mock_select.assert_not_called()  # select ne devrait pas être appelé car on n'appelle pas execute()
