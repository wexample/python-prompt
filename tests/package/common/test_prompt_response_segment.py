from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.text_style import TextStyle
from wexample_prompt.enums.terminal_color import TerminalColor


class TestPromptResponseSegment:
    def test_create_basic_segment(self):
        """Test creating a basic text segment without styling."""
        segment = PromptResponseSegment(text="Hello")
        assert segment.text == "Hello"

    def test_empty_text(self):
        """Test that empty text is allowed."""
        segment = PromptResponseSegment(text="")
        assert segment.text == ""

    def test_render_with_styles_and_colorized(self):
        segment = PromptResponseSegment(
            text="Hello",
            color=TerminalColor.GREEN,
            styles=[TextStyle.BOLD, TextStyle.UNDERLINE],
        )
        context = PromptContext(colorized=True, width=80)
        rendered, remainder = segment.render(context=context, line_remaining_width=80)
        assert remainder is None
        assert "Hello" in rendered
        assert str(TerminalColor.GREEN) in rendered
        assert "\033[1m" in rendered  # bold
        assert "\033[4m" in rendered  # underline
        assert rendered.endswith("\033[0m")

    def test_render_without_colorized(self):
        segment = PromptResponseSegment(
            text="Hello", color=TerminalColor.GREEN, styles=[TextStyle.BOLD]
        )
        context = PromptContext(colorized=False, width=80)
        rendered, remainder = segment.render(context=context, line_remaining_width=80)
        assert remainder is None
        assert rendered == "Hello"

    def test_render_wrap_preserves_styles(self):
        segment = PromptResponseSegment(
            text="HelloWorld", color=TerminalColor.RED, styles=[TextStyle.ITALIC]
        )
        context = PromptContext(colorized=True, width=80)
        # Force wrap after 5 characters
        rendered1, remainder = segment.render(context=context, line_remaining_width=5)
        assert remainder is not None
        assert "Hello" in rendered1
        assert str(TerminalColor.RED) in rendered1
        assert "\033[3m" in rendered1  # italic
        assert rendered1.endswith("\033[0m")
        # Render remainder on next line
        rendered2, remainder2 = remainder.render(
            context=context, line_remaining_width=80
        )
        assert remainder2 is None
        assert "World" in rendered2
        assert str(TerminalColor.RED) in rendered2
        assert "\033[3m" in rendered2
        assert rendered2.endswith("\033[0m")
