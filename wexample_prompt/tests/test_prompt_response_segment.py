import pytest
from pydantic import ValidationError

from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.enums.text_style import TextStyle
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment


class TestPromptResponseSegment:
    def test_create_basic_segment(self):
        """Test creating a basic text segment without styling."""
        segment = PromptResponseSegment(text="Hello")
        assert segment.text == "Hello"
        assert segment.styles == []

    def test_create_styled_segment(self):
        """Test creating a segment with styling."""
        segment = PromptResponseSegment(
            text="Bold Text",
            styles=[TextStyle.BOLD]
        )
        assert segment.text == "Bold Text"
        assert TextStyle.BOLD in segment.styles

    def test_multiple_styles(self):
        """Test segment with multiple styles."""
        segment = PromptResponseSegment(
            text="Bold and Italic",
            styles=[TextStyle.BOLD, TextStyle.ITALIC]
        )
        assert len(segment.styles) == 2
        assert TextStyle.BOLD in segment.styles
        assert TextStyle.ITALIC in segment.styles

    def test_empty_text(self):
        """Test that empty text is allowed."""
        segment = PromptResponseSegment(text="")
        assert segment.text == ""

    def test_invalid_style(self):
        """Test that invalid styles raise validation error."""
        with pytest.raises(ValidationError):
            PromptResponseSegment(
                text="Test",
                styles=["invalid_style"]
            )

    def test_segment_equality(self):
        """Test segment equality comparison."""
        seg1 = PromptResponseSegment(text="Test", styles=[TextStyle.BOLD])
        seg2 = PromptResponseSegment(text="Test", styles=[TextStyle.BOLD])
        seg3 = PromptResponseSegment(text="Different", styles=[TextStyle.BOLD])
        
        assert seg1 == seg2
        assert seg1 != seg3

    def test_segment_combination(self):
        """Test combining two segments."""
        seg1 = PromptResponseSegment(text="Bold", styles=[TextStyle.BOLD])
        seg2 = PromptResponseSegment(text=" and Italic", styles=[TextStyle.ITALIC])
        
        combined = seg1.combine(seg2)
        assert combined.text == "Bold and Italic"
        assert TextStyle.BOLD in combined.styles
        assert TextStyle.ITALIC in combined.styles
