import pytest
from pydantic import ValidationError

from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.enums.text_style import TextStyle
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_layout import PromptLayout


class TestPromptResponseLine:
    def test_create_basic_line(self):
        """Test creating a basic line with single segment."""
        segment = PromptResponseSegment(text="Hello")
        line = PromptResponseLine(segments=[segment])
        assert len(line.segments) == 1
        assert line.segments[0].text == "Hello"

    def test_create_styled_line(self):
        """Test creating a line with styled segments."""
        segments = [
            PromptResponseSegment(text="Bold", styles=[TextStyle.BOLD]),
            PromptResponseSegment(text=" and ", styles=[]),
            PromptResponseSegment(text="Italic", styles=[TextStyle.ITALIC])
        ]
        line = PromptResponseLine(segments=segments)
        assert len(line.segments) == 3
        assert line.segments[0].styles == [TextStyle.BOLD]
        assert line.segments[2].styles == [TextStyle.ITALIC]

    def test_line_with_type(self):
        """Test line with message type."""
        segment = PromptResponseSegment(text="Error")
        line = PromptResponseLine(
            segments=[segment],
            line_type=MessageType.ERROR
        )
        assert line.line_type == MessageType.ERROR

    def test_line_with_layout(self):
        """Test line with layout settings."""
        segment = PromptResponseSegment(text="Centered")
        layout = PromptLayout(padding=2, margin=1, width=20)
        line = PromptResponseLine(
            segments=[segment],
            layout=layout
        )
        assert line.layout.padding == 2
        assert line.layout.margin == 1
        assert line.layout.width == 20

    def test_empty_line(self):
        """Test that line must have at least one segment."""
        with pytest.raises(ValidationError):
            PromptResponseLine(segments=[])

    def test_line_indentation(self):
        """Test line indentation."""
        segment = PromptResponseSegment(text="Indented")
        line = PromptResponseLine(
            segments=[segment],
            indent_level=2
        )
        assert line.indent_level == 2

    def test_line_combination(self):
        """Test combining two lines."""
        line1 = PromptResponseLine(segments=[
            PromptResponseSegment(text="First")
        ])
        line2 = PromptResponseLine(segments=[
            PromptResponseSegment(text="Second")
        ])
        combined = line1.combine(line2)
        assert len(combined.segments) == 2
        assert combined.segments[0].text == "First"
        assert combined.segments[1].text == "Second"

    def test_line_to_string(self):
        """Test converting line to string."""
        segments = [
            PromptResponseSegment(text="Hello"),
            PromptResponseSegment(text=" World")
        ]
        line = PromptResponseLine(segments=segments)
        assert str(line) == "Hello World"
