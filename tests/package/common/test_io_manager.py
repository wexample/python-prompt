from wexample_prompt.testing.abstract_prompt_test import AbstractPromptTest


class TestIoManager(AbstractPromptTest):
    def test_echo_width(self):
        assert self._io.terminal_width is not None

        # Echo a string using the terminal with length
        rendered = self._io.echo(message=(self._io.terminal_width * "!"))
        # It should print only one line.
        self._assert_rendered_lines_count(rendered=rendered, lines_count=1)

    def test_progress_width(self):
        # Echo a string using the terminal with length
        rendered = self._io.progress(
            total=20,
            current=10
        )
        self._assert_rendered_lines_count(rendered=rendered, lines_count=1)

        rendered = self._io.progress(
            label="With a label",
            total=20,
            current=10
        )
        self._assert_rendered_lines_count(rendered=rendered, lines_count=1)

    def _assert_rendered_lines_count(self, rendered: str, lines_count: int):
        assert len(rendered.split("\n")) == lines_count
