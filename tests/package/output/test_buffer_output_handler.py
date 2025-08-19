"""Tests for BufferOutputHandler."""
from wexample_prompt.output.buffer_output_handler import BufferOutputHandler
from wexample_prompt.testing.abstract_prompt_test import AbstractPromptTest


class TestBufferOutputHandler(AbstractPromptTest):
    def test_print_buffers_response_and_returns_rendered(self):
        # Switch IoManager to buffer output handler
        self._io.output = BufferOutputHandler()

        # Call a simple echo to produce a response
        rendered = self._io.echo("Buffered output")

        # Should return a string (rendered output)
        assert isinstance(rendered, str)
        assert "Buffered output" in rendered

        # Buffer should contain exactly one response object
        assert isinstance(self._io.output, BufferOutputHandler)
        assert len(self._io.output.buffer) == 1

        # The buffered item should be a response with matching render
        buffered_response = self._io.output.buffer[0]
        assert buffered_response.render() == rendered
