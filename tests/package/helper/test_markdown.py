"""Tests for the markdown -> ANSI/OSC8 helper."""

from __future__ import annotations

from wexample_prompt.helper.markdown import markdown_to_ansi
from wexample_prompt.helper.terminal import terminal_get_visible_width


def test_blockquote_dims_the_pipe_and_renders_inline_styles() -> None:
    out = markdown_to_ansi("> Stay **focused**")
    visible = _visible(out)
    assert visible.startswith("│ ")
    assert "focused" in visible
    assert "\x1b[1m" in out  # inline bold still kicks in


def test_blockquote_multiline_each_line_prefixed() -> None:
    out = markdown_to_ansi("> line one\n> line two")
    lines = _visible(out).split("\n")
    assert all(line.startswith("│ ") for line in lines)


def test_bold_does_not_eat_italic() -> None:
    """`**x**` must NOT also match `*x*` — order of substitutions matters."""
    out = markdown_to_ansi("**bold** and *ita*")
    # Both styles present, bold opening followed by closing before italic.
    assert out.count("\x1b[1m") == 1
    assert out.count("\x1b[3m") == 1


def test_bold_star_emits_ansi_bold() -> None:
    out = markdown_to_ansi("hello **world**")
    assert "\x1b[1m" in out and "\x1b[22m" in out
    assert _visible(out) == "hello world"


def test_bold_underscore_emits_ansi_bold() -> None:
    out = markdown_to_ansi("__strong__ stuff")
    assert "\x1b[1m" in out
    assert _visible(out) == "strong stuff"


def test_bullet_list_renders_round_bullet() -> None:
    out = markdown_to_ansi("- first\n- second")
    visible = _visible(out)
    assert "• first" in visible
    assert "• second" in visible


def test_empty_string_returns_empty() -> None:
    assert markdown_to_ansi("") == ""


def test_fenced_code_block_uses_dim_and_indent() -> None:
    src = "```\ndef f():\n    return 1\n```"
    out = markdown_to_ansi(src)
    visible = _visible(out)
    # Fence markers themselves are gone.
    assert "```" not in visible
    # Code body is indented two spaces.
    assert "  def f():" in visible
    assert "      return 1" in visible
    assert "\x1b[2m" in out


def test_h1_is_bold_underlined() -> None:
    out = markdown_to_ansi("# Title")
    assert "\x1b[1m" in out
    assert "\x1b[4m" in out
    assert "Title" in _visible(out)


def test_h2_is_bold_only() -> None:
    out = markdown_to_ansi("## Sub")
    assert "\x1b[1m" in out
    assert "\x1b[4m" not in out


def test_h3_uses_dim_marker_with_bold_label() -> None:
    out = markdown_to_ansi("### Section")
    assert "\x1b[2m" in out  # dim around marker
    assert "\x1b[1m" in out  # bold label


def test_horizontal_rule() -> None:
    out = markdown_to_ansi("---", hr_width=10)
    assert "──────────" in _visible(out)
    assert "\x1b[2m" in out


def test_image_is_rendered_as_label_not_hyperlink() -> None:
    out = markdown_to_ansi("![screenshot](https://example.com/x.png)")
    assert "[image: screenshot]" in _visible(out)
    # No OSC 8 sequence — images are NOT clickable in a terminal.
    assert "\x1b]8;;" not in out


def test_image_with_empty_alt_falls_back_to_url() -> None:
    out = markdown_to_ansi("![](https://example.com/x.png)")
    assert "https://example.com/x.png" in _visible(out)


def test_inline_code_uses_dim_underline() -> None:
    """Inline code reads as a literal token without screaming like reverse video."""
    out = markdown_to_ansi("use`pytest`now")
    assert "\x1b[2m" in out  # dim
    assert "\x1b[4m" in out  # underline
    assert "\x1b[7m" not in out  # NOT reverse video
    # No injected padding spaces around the code body — visible payload
    # must match the source character-for-character.
    assert _visible(out) == "usepytestnow"


def test_italic_star_emits_ansi_italic() -> None:
    out = markdown_to_ansi("a *thing* here")
    assert "\x1b[3m" in out and "\x1b[23m" in out
    assert _visible(out) == "a thing here"


def test_link_becomes_osc8_hyperlink_with_underline_fallback() -> None:
    out = markdown_to_ansi("see [docs](https://example.com)")
    # OSC 8 start sequence + URL + ST.
    assert "\x1b]8;;https://example.com\x1b\\" in out
    # Underline so the link still reads as a link in dumb terms.
    assert "\x1b[4m" in out
    # Visible width counts label, not URL.
    assert terminal_get_visible_width(out) == len("see docs")


def test_numbered_list_preserves_index() -> None:
    out = markdown_to_ansi("1. one\n2. two")
    visible = _visible(out)
    assert "1. one" in visible
    assert "2. two" in visible


def test_plain_text_passes_through_untouched() -> None:
    assert markdown_to_ansi("hello world") == "hello world"


def test_strikethrough() -> None:
    out = markdown_to_ansi("~~gone~~")
    assert "\x1b[9m" in out
    assert _visible(out) == "gone"


def test_visible_width_compatible_with_terminal_helper() -> None:
    """`terminal_get_visible_width` must see the same column count as a human."""
    out = markdown_to_ansi("**a** [b](http://x) c")
    # Visible = "a b c" = 5 columns.
    assert terminal_get_visible_width(out) == 5


def _visible(text: str) -> str:
    """Strip ANSI/OSC sequences so assertions read against plain content."""
    from wexample_helpers.const.terminal import OSC_SEQUENCE_RE
    from wexample_helpers.helpers.ansi import ansi_strip

    return OSC_SEQUENCE_RE.sub("", ansi_strip(text))
