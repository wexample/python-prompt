"""Test multiple prompt response."""
from abc import abstractmethod
from typing import Type
from unittest.mock import patch

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.responses.data.multiple_prompt_response import MultiplePromptResponse
from wexample_prompt.responses.messages.log_prompt_response import LogPromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest


class TestMultiplePromptResponse(AbstractPromptResponseTest):
    """Test multiple prompt response."""

    test_message = "Test message"
    class_with_context = MultiplePromptResponse

    def setUp(self):
        """Set up test cases."""
        super().setUp()
        self.test_responses = [
            LogPromptResponse.create_log("First response", context=self.context),
            LogPromptResponse.create_log("Item 1", context=self.context),
            LogPromptResponse.create_log("Item 2", context=self.context),
            LogPromptResponse.create_log("Last response", context=self.context)
        ]

    def get_response_class(self) -> Type[AbstractPromptResponse]:
        """Get the response class being tested.

        Returns:
            Type[AbstractPromptResponse]: The response class
        """
        return MultiplePromptResponse

    def get_io_method_name(self) -> str:
        """Get the name of the IO manager method for this response type.

        Returns:
            str: The method name
        """
        return 'multiple'

    def _assert_specific_format(self, rendered: str):
        """Assert format specific to this response type."""
        pass

    def get_expected_lines(self) -> int:
        """Get expected number of lines in rendered output."""
        return 1  # Just the list item for test_message

    def assert_common_response_structure(self, rendered: str):
        """Assert that the rendered response has the expected structure.

        Args:
            rendered: The rendered response to check
        """
        self.assert_contains_text(rendered, self.test_message)

    def create_test_response(self, text: str, **kwargs) -> MultiplePromptResponse:
        """Create a test response.

        Args:
            text: Text for the response
            **kwargs: Additional arguments passed to the constructor

        Returns:
            MultiplePromptResponse: A new test response instance
        """
        context = kwargs.pop('context', self.context)
        return MultiplePromptResponse.create_multiple(
            responses=[LogPromptResponse.create_log(text, context=context)],
            context=context,
            **kwargs
        )

    def test_empty_responses(self):
        """Test empty multiple response."""
        response = MultiplePromptResponse.create_multiple(
            responses=[],
            context=self.context
        )
        self.assertEqual(response.render(), "")

    def test_single_response(self):
        """Test multiple response with a single response."""
        response = self.create_test_response(self.test_message)
        self.assertEqual(response.render(), self.test_message)

    def test_multiple_responses(self):
        """Test multiple responses."""
        response = MultiplePromptResponse.create_multiple(
            responses=self.test_responses,
            context=self.context
        )
        self.assertEqual(
            response.render(),
            "First response\nItem 1\nItem 2\nLast response"
        )

    def test_append_response(self):
        """Test appending a response."""
        response = MultiplePromptResponse.create_multiple(
            responses=[LogPromptResponse.create_log("Initial", context=self.context)],
            context=self.context
        )
        response.append_response(LogPromptResponse.create_log("Appended", context=self.context))
        self.assertEqual(response.render(), "Initial\nAppended")

    def test_extend_responses(self):
        """Test extending with multiple responses."""
        response = MultiplePromptResponse.create_multiple(
            responses=[LogPromptResponse.create_log("Initial", context=self.context)],
            context=self.context
        )
        response.extend_responses([
            LogPromptResponse.create_log("Extended 1", context=self.context),
            LogPromptResponse.create_log("Extended 2", context=self.context)
        ])
        self.assertEqual(response.render(), "Initial\nExtended 1\nExtended 2")

    def test_io_manager(self):
        """Test IoManager integration."""
        result = self.io.multiple(
            responses=self.test_responses
        )
        self.assertIsInstance(result, MultiplePromptResponse)
        self.assertEqual(
            result.render(),
            "First response\nItem 1\nItem 2\nLast response"
        )

    def test_prompt_context(self):
        """Test PromptContext implementation."""
        context = self.context
        class_with_context = self.class_with_context
        self.assertTrue(hasattr(class_with_context, 'multiple'))

    @patch('wexample_prompt.common.color_manager.ColorManager.supports_color')
    def test_custom_color(self, mock_supports_color):
        """Test response with custom color."""
        context = self.create_colored_test_context(mock_supports_color)
        response = self.create_test_response(self.test_message, context=context, color=TerminalColor.GREEN)
        rendered = response.render()
        self.assert_contains_text(rendered, self.test_message)

    def test_no_color(self):
        """Test response without color."""
        response = self.create_test_response(self.test_message, color=None)
        rendered = response.render()
        self.assert_contains_text(rendered, self.test_message)

    def test_response_class(self):
        """Test response class behavior."""
        response = self.create_test_response(self.test_message)
        rendered = response.render()
        self.assert_contains_text(rendered, self.test_message)
