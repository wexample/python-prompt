from typing import TYPE_CHECKING

from wexample_prompt.testing.abstract_prompt_test import AbstractPromptTest

if TYPE_CHECKING:
    from wexample_app.response.abstract_response import AbstractResponse


class TestIoManager(AbstractPromptTest):
    def test_echo_width(self):
        assert self._io.terminal_width is not None

        # Echo a string using the terminal with length
        response = self._io.echo(message=(self._io.terminal_width * "!"))
        # It should print only one line.
        self._assert_rendered_lines_count(response=response, lines_count=1)

    def test_progress_width(self):
        # Echo a string using the terminal with length
        response = self._io.progress(
            total=20,
            current=10
        )
        self._assert_rendered_lines_count(response=response, lines_count=1)

        response = self._io.progress(
            label="With a label",
            total=20,
            current=10
        )
        self._assert_rendered_lines_count(response=response, lines_count=1)

    def _assert_rendered_lines_count(self, response: "AbstractResponse", lines_count: int):
        assert len(response.last_rendered_content.split("\n")) == lines_count
