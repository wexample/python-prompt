from wexample_prompt.common.prompt_response_segment import PromptResponseSegment


class TestPromptResponseSegment:
    def test_create_basic_segment(self):
        """Test creating a basic text segment without styling."""
        segment = PromptResponseSegment(text="Hello")
        assert segment.text == "Hello"

    def test_empty_text(self):
        """Test that empty text is allowed."""
        segment = PromptResponseSegment(text="")
        assert segment.text == ""
