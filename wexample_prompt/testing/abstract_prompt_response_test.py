"""Base class for testing prompt responses."""
from abc import abstractmethod

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.testing.abstract_prompt_test import AbstractPromptTest


class AbstractPromptResponseTest(AbstractPromptTest):

    @abstractmethod
    def get_expected_lines(self) -> int:
        """Return the expected number of lines in the rendered response."""
        pass

    @abstractmethod
    def create_test_response(self, **kwargs) -> AbstractPromptResponse:
        """Create a response instance."""
        pass

    def _assert_common_response_structure(self, rendered: str):
        """Assert common structure for rendered responses."""
        lines = rendered.split("\n")
        expected_lines = self.get_expected_lines()

        self.assertEqual(len(lines), expected_lines)

        # If more than one line, first should be empty
        if expected_lines > 1:
            self.assertEqual(lines[0].strip(), "")

    @abstractmethod
    def _assert_specific_format(self, rendered: str):
        """Assert format specific to this response type."""
        pass

    def test_response_class(self):
        """Test response class behavior."""
        response = self.create_test_response()
        rendered = response.render()

        self._assert_common_response_structure(rendered)
        self._assert_contains_text(rendered, self._test_message)
        self._assert_specific_format(rendered)


    def test_verbosity(self):
        from wexample_prompt.common.prompt_context import PromptContext
        from wexample_prompt.enums.verbosity_level import VerbosityLevel

        response = self.create_test_response(
            verbosity=VerbosityLevel.MAXIMUM
        )

        rendered = response.render(
            context=PromptContext(
                verbosity=VerbosityLevel.QUIET
            )
        )

        assert rendered is None
