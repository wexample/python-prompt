"""Base class for testing prompt responses."""
from abc import abstractmethod

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.testing.abstract_prompt_test import AbstractPromptTest


class AbstractPromptResponseTest(AbstractPromptTest):

    @abstractmethod
    def get_expected_lines(self) -> int:
        """Return the expected number of lines in the rendered response."""
        pass

    def assert_common_response_structure(self, rendered: str):
        """Assert common structure for rendered responses."""
        lines = rendered.split("\n")
        expected_lines = self.get_expected_lines()

        self.assertEqual(len(lines), expected_lines)

        # If more than one line, first should be empty
        if expected_lines > 1:
            self.assertEqual(lines[0].strip(), "")

    def assert_contains_text(self, rendered: str, text: str):
        """Assert that rendered output contains specific text."""
        self.assertIn(text, rendered)

    @abstractmethod
    def create_test_response(self, text: str, **kwargs) -> AbstractPromptResponse:
        """Create a response instance."""
        pass

    @abstractmethod
    def _assert_specific_format(self, rendered: str):
        """Assert format specific to this response type."""
        pass

    def test_response_class(self):
        """Test response class behavior."""
        response = self.create_test_response(self._test_message)
        rendered = response.render()

        self.assert_common_response_structure(rendered)
        self.assert_contains_text(rendered, self._test_message)
        self._assert_specific_format(rendered)

