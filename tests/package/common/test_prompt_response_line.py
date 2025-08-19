from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment


class TestPromptResponseLine:
    def test_create_basic_line(self):
        """Test creating a basic line with single segment."""
        segment = PromptResponseSegment(text="Hello")
        line = PromptResponseLine(segments=[segment])
        assert len(line.segments) == 1
        assert line.segments[0].text == "Hello"

    def test_line_to_string(self):
        from wexample_prompt.common.prompt_context import PromptContext

        """Test converting line to string."""
        segments = [
            PromptResponseSegment(text="Hello"),
            PromptResponseSegment(text=" World")
        ]
        line = PromptResponseLine(segments=segments)
        assert line.render(context=PromptContext()) == "Hello World"
