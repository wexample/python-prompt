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

    def _assert_no_color_codes(self, text: str):
        """Assert that a string contains no ANSI escape sequences (colors/styles)."""
        import re
        # Generic ANSI escape sequence regex (covers CSI, OSC, and single-char escapes)
        ansi_pattern = re.compile(
            r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])"
        )
        assert not ansi_pattern.search(text), f"Unexpected ANSI escape sequences found in: {text!r}"

    def test_response_class(self):
        """Test response class behavior."""
        response = self.create_test_response()
        rendered = response.render()

        self._assert_common_response_structure(rendered)
        self._assert_contains_text(rendered, self._test_message)
        self._assert_specific_format(rendered)


    def test_no_color(self):
        from wexample_prompt.common.prompt_context import PromptContext
        response = self.create_test_response()
        rendered = response.render(context=PromptContext(colorized=False))
        self._assert_no_color_codes(rendered)

    def test_verbosity(self):
        from wexample_prompt.common.prompt_context import PromptContext
        from wexample_prompt.enums.verbosity_level import VerbosityLevel

        # Contexts with different verbosity levels
        quiet_context = PromptContext(verbosity=VerbosityLevel.QUIET)
        default_context = PromptContext(verbosity=VerbosityLevel.DEFAULT)
        medium_context = PromptContext(verbosity=VerbosityLevel.MEDIUM)
        max_context = PromptContext(verbosity=VerbosityLevel.MAXIMUM)

        # Responses requiring different verbosity thresholds
        quiet_required = self.create_test_response(verbosity=VerbosityLevel.QUIET)
        default_required = self.create_test_response(verbosity=VerbosityLevel.DEFAULT)
        maximum_required = self.create_test_response(verbosity=VerbosityLevel.MAXIMUM)

        def assert_visibility(context, expectations):
            # expectations: list of tuples (response, should_be_visible)
            for response, should_be_visible in expectations:
                rendered = response.render(context=context)
                if should_be_visible:
                    assert rendered is not None
                    self._assert_contains_text(rendered, self._test_message)
                else:
                    assert rendered is None

        # Quiet context: only QUIET-level responses should appear
        assert_visibility(quiet_context, [
            (quiet_required, True),
            (default_required, False),
            (maximum_required, False),
        ])

        # Default context: QUIET and DEFAULT appear; MAXIMUM hidden
        assert_visibility(default_context, [
            (quiet_required, True),
            (default_required, True),
            (maximum_required, False),
        ])

        # Medium context: QUIET, DEFAULT, MEDIUM appear; MAXIMUM hidden
        medium_required = self.create_test_response(verbosity=VerbosityLevel.MEDIUM)
        assert_visibility(medium_context, [
            (quiet_required, True),
            (default_required, True),
            (medium_required, True),
            (maximum_required, False),
        ])

        # Maximum context: all appear
        assert_visibility(max_context, [
            (quiet_required, True),
            (default_required, True),
            (maximum_required, True),
        ])

    def test_manager_indentation(self):
        response = self.create_test_response()

        rendered = self._io.print_response(
            response=response
        )

        assert isinstance(rendered, str)
        assert not rendered.startswith("  ")

        self._io.indentation_up()

        rendered = self._io.print_response(
            response=response
        )

        assert isinstance(rendered, str)
        assert rendered.startswith("  ")

        self._io.indentation_up()

        rendered = self._io.print_response(
            response=response
        )

        assert isinstance(rendered, str)
        assert rendered.startswith("    ")

        self._io.indentation_down()
        self._io.indentation_down()

        rendered = self._io.print_response(
            response=response
        )

        assert isinstance(rendered, str)
        assert not rendered.startswith("  ")

