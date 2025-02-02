"""Tests for MultiplePromptResponse."""
from typing import Type

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.responses.data.list_prompt_response import ListPromptResponse
from wexample_prompt.responses.data.multiple_prompt_response import MultiplePromptResponse
from wexample_prompt.responses.messages.log_prompt_response import LogPromptResponse
from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest


class TestMultiplePromptResponse(AbstractPromptResponseTest):
    """Test cases for MultiplePromptResponse."""

    class_with_context = MultiplePromptResponse

    def setUp(self):
        """Set up test cases."""
        super().setUp()
        self.test_message = "Test message"
        self.test_responses = [
            LogPromptResponse.create_log("First response", context=self.context),
            ListPromptResponse.create_list(items=["Item 1", "Item 2"], context=self.context),
            LogPromptResponse.create_log("Last response", context=self.context)
        ]

    def get_response_class(self) -> Type[AbstractPromptResponse]:
        """Get the response class being tested."""
        return MultiplePromptResponse

    def get_io_method_name(self) -> str:
        """Get the name of the IO manager method for this response type."""
        return 'multiple'

    def _assert_specific_format(self, rendered: str):
        """Assert specific format for multiple responses."""
        # Each response should be rendered on its own line
        self.assertTrue("\n" in rendered)

    def get_expected_lines(self) -> int:
        """Get expected number of lines in rendered output."""
        return 3  # One line for each test response

    def assert_common_response_structure(self, rendered: str):
        """Assert the common structure for multiple responses."""
        self.assert_contains_text(rendered, "First response")
        self.assert_contains_text(rendered, "Last response")

    def create_test_response(self, text: str, **kwargs) -> MultiplePromptResponse:
        """Create a test multiple response.

        Args:
            text: Text to display
            **kwargs: Additional arguments

        Returns:
            MultiplePromptResponse: Test response
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
        rendered = response.render()
        self.assertEqual(rendered.strip(), "")

    def test_single_response(self):
        """Test multiple response with a single response."""
        response = self.create_test_response(self.test_message)
        rendered = response.render()
        self.assert_contains_text(rendered, self.test_message)

    def test_multiple_responses(self):
        """Test multiple responses."""
        response = MultiplePromptResponse.create_multiple(
            responses=self.test_responses,
            context=self.context
        )
        rendered = response.render()
        self.assert_contains_text(rendered, "First response")
        self.assert_contains_text(rendered, "Item 1")
        self.assert_contains_text(rendered, "Item 2")
        self.assert_contains_text(rendered, "Last response")

    def test_append_response(self):
        """Test appending a response."""
        response = MultiplePromptResponse.create_multiple(
            responses=[LogPromptResponse.create_log("Initial", context=self.context)],
            context=self.context
        )
        response.append_response(LogPromptResponse.create_log("Appended", context=self.context))
        rendered = response.render()
        self.assert_contains_text(rendered, "Initial")
        self.assert_contains_text(rendered, "Appended")

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
        rendered = response.render()
        self.assert_contains_text(rendered, "Initial")
        self.assert_contains_text(rendered, "Extended 1")
        self.assert_contains_text(rendered, "Extended 2")

    def test_io_manager(self):
        """Test IoManager integration."""
        result = self.io_manager.multiple(
            responses=self.test_responses
        )
        self.assertIsInstance(result, MultiplePromptResponse)
        rendered = result.render()
        self.assert_contains_text(rendered, "First response")
        self.assert_contains_text(rendered, "Last response")

    def test_prompt_context(self):
        """Test PromptContext implementation."""
        context = self.context
        class_with_context = self.class_with_context
        method = getattr(class_with_context, self.get_io_method_name())
        response = method(responses=self.test_responses)
        rendered = response.render()
        self.assert_contains_text(rendered, "First response")
        self.assert_contains_text(rendered, "Last response")
