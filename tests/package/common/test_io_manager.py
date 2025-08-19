from wexample_prompt.testing.abstract_prompt_test import AbstractPromptTest


class TestIoManager(AbstractPromptTest):
    def test_create_basic_line(self):
        assert self._io.terminal_width is not None

        # Echo a string using the terminal with length
        rendered = self._io.echo(message=(self._io.terminal_width * "!"))
        # It should print only one line.
        assert len(rendered.split("\n")) == 1
