"""
Benchmarks for wexample_prompt critical path.

Run with:
    pytest tests/performance/test_benchmark.py --benchmark-only

Each benchmark targets a function that is called frequently or sits on the
hot path of the rendering pipeline (parsing → segment building → line render).
Constructors and trivial accessors are excluded.
"""

from __future__ import annotations

import pytest

from wexample_prompt.common.color_manager import ColorManager
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.common.style_markup_parser import flatten_style_markup, parse_style_markup
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.enums.text_style import TextStyle
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.responses.data.table_prompt_response import TablePromptResponse


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

CTX_DEFAULT = PromptContext()
CTX_COLORIZED = PromptContext(colorized=True, width=80)
CTX_WRAPPED = PromptContext(colorized=True, formatting=True, width=40)
CTX_WIDE = PromptContext(colorized=True, formatting=True, width=120)

PLAIN_TEXT = "The quick brown fox jumps over the lazy dog."
MARKUP_SIMPLE = "Hello @color:red{World} and @color:blue+bold{sky}."
MARKUP_COMPLEX = (
    "@color:blue+bold{Outer @color:yellow+underline{Inner} text} "
    "@🔵{Blue} @🟢+bold{Green} end @color:red{red @color:white+italic{nested white}}"
)
MARKUP_LONG = " ".join(
    [f"@color:red{{{i}}} word @color:blue+bold{{item-{i}}}" for i in range(20)]
)
MULTILINE_TEXT = "\n".join([f"Line number {i}: some content here" for i in range(10)])

# Pre-built objects reused across rendering benchmarks
_SIMPLE_LINE = PromptResponseLine.create_from_string(PLAIN_TEXT)[0]
_MARKUP_LINE = PromptResponseLine.create_from_string(MARKUP_SIMPLE)[0]
_COLORED_SEGMENT = PromptResponseSegment(
    text="Hello World", color=TerminalColor.GREEN, styles=[TextStyle.BOLD, TextStyle.UNDERLINE]
)
_PLAIN_SEGMENT = PromptResponseSegment(text="Hello World")
_LONG_SEGMENT = PromptResponseSegment(text="A" * 200, color=TerminalColor.CYAN)

_RESPONSE_LINES = PromptResponseLine.create_from_string(MULTILINE_TEXT)


# ---------------------------------------------------------------------------
# parse_style_markup  — regex + recursive descent, called for every text input
# ---------------------------------------------------------------------------

def test_parse_markup_plain_text(benchmark):
    """Baseline: parsing overhead on text with no directives."""
    benchmark(parse_style_markup, PLAIN_TEXT)


def test_parse_markup_simple_colors(benchmark):
    """Simple color + bold markup; exercises regex match and apply_tokens."""
    benchmark(parse_style_markup, MARKUP_SIMPLE)


def test_parse_markup_complex_nested(benchmark):
    """Deeply nested directives including emoji colors and style combinations."""
    benchmark(parse_style_markup, MARKUP_COMPLEX)


def test_parse_markup_long_many_directives(benchmark):
    """Many directives in sequence; stresses the scanning loop."""
    benchmark(parse_style_markup, MARKUP_LONG)


# ---------------------------------------------------------------------------
# flatten_style_markup  — parse + flatten; used by table cell rendering
# ---------------------------------------------------------------------------

def test_flatten_markup_simple(benchmark):
    """flatten_style_markup on a single-line markup string."""
    benchmark(flatten_style_markup, MARKUP_SIMPLE)


def test_flatten_markup_complex(benchmark):
    """flatten_style_markup on complex nested markup."""
    benchmark(flatten_style_markup, MARKUP_COMPLEX)


# ---------------------------------------------------------------------------
# PromptResponseLine.create_from_string  — parse + segment construction
# ---------------------------------------------------------------------------

def test_line_create_from_plain_string(benchmark):
    """Plain string with no markup; measures pure segment construction overhead."""
    benchmark(PromptResponseLine.create_from_string, PLAIN_TEXT)


def test_line_create_from_markup_string(benchmark):
    """String with inline color/style markup."""
    benchmark(PromptResponseLine.create_from_string, MARKUP_SIMPLE)


def test_line_create_from_multiline_string(benchmark):
    """Multi-line input; produces multiple PromptResponseLine objects."""
    benchmark(PromptResponseLine.create_from_string, MULTILINE_TEXT)


# ---------------------------------------------------------------------------
# PromptResponseLine.render  — hot path: renders each line on every print call
# ---------------------------------------------------------------------------

def test_line_render_no_formatting(benchmark):
    """Render a plain line without wrapping (formatting=False, default path)."""
    benchmark(_SIMPLE_LINE.render, CTX_DEFAULT)


def test_line_render_markup_no_formatting(benchmark):
    """Render a markup line; exercises colorize path but no wrap."""
    benchmark(_MARKUP_LINE.render, CTX_COLORIZED)


def test_line_render_wrapped_short_width(benchmark):
    """Render with wrapping enabled at narrow width (40 chars); many splits."""
    long_line = PromptResponseLine.create_from_string("A" * 200)[0]
    benchmark(long_line.render, CTX_WRAPPED)


def test_line_render_wrapped_with_markup(benchmark):
    """Render a colorized markup line with wrapping enabled."""
    line = PromptResponseLine.create_from_string(MARKUP_COMPLEX)[0]
    benchmark(line.render, CTX_WRAPPED)


# ---------------------------------------------------------------------------
# PromptResponseSegment.render  — innermost rendering unit, called per segment
# ---------------------------------------------------------------------------

def test_segment_render_colorized(benchmark):
    """Render a colored + styled segment; exercises ColorManager.build_prefix."""
    benchmark(_COLORED_SEGMENT.render, CTX_COLORIZED, 80)


def test_segment_render_no_color(benchmark):
    """Render a plain segment without colors (fast path)."""
    benchmark(_PLAIN_SEGMENT.render, CTX_DEFAULT, 80)


def test_segment_render_with_split(benchmark):
    """Render a long segment that must be split across a narrow width."""
    benchmark(_LONG_SEGMENT.render, CTX_COLORIZED, 40)


# ---------------------------------------------------------------------------
# ColorManager.build_prefix  — called for every colored segment on every render
# ---------------------------------------------------------------------------

def test_color_manager_build_prefix_color_only(benchmark):
    """Build an ANSI prefix for a color with no extra styles."""
    benchmark(ColorManager.build_prefix, color=TerminalColor.RED)


def test_color_manager_build_prefix_color_and_styles(benchmark):
    """Build an ANSI prefix combining color with multiple text styles."""
    benchmark(
        ColorManager.build_prefix,
        color=TerminalColor.BLUE,
        styles=[TextStyle.BOLD, TextStyle.UNDERLINE, TextStyle.ITALIC],
    )


# ---------------------------------------------------------------------------
# AbstractPromptResponse.render  — top-level orchestrator, joins all lines
# ---------------------------------------------------------------------------

def _make_echo_response(n_lines: int) -> AbstractPromptResponse:
    from wexample_prompt.responses.echo_prompt_response import EchoPromptResponse

    lines = PromptResponseLine.create_from_string(
        "\n".join(f"Line {i}: some content" for i in range(n_lines))
    )
    return EchoPromptResponse(lines=lines)


_RESPONSE_1 = _make_echo_response(1)
_RESPONSE_10 = _make_echo_response(10)
_RESPONSE_50 = _make_echo_response(50)


def test_response_render_single_line(benchmark):
    """Render a one-line response (minimum viable case)."""
    benchmark(_RESPONSE_1.render, CTX_COLORIZED)


def test_response_render_ten_lines(benchmark):
    """Render a response with 10 lines; exercises the join loop."""
    benchmark(_RESPONSE_10.render, CTX_COLORIZED)


def test_response_render_fifty_lines(benchmark):
    """Render a 50-line response; stresses the full per-line pipeline."""
    benchmark(_RESPONSE_50.render, CTX_COLORIZED)


# ---------------------------------------------------------------------------
# TablePromptResponse.render  — full table pipeline including column widths
# ---------------------------------------------------------------------------

_SMALL_TABLE_DATA = [[f"cell-{r}-{c}" for c in range(3)] for r in range(5)]
_LARGE_TABLE_DATA = [[f"value_{r}_{c}" for c in range(8)] for r in range(20)]
_STYLED_TABLE_DATA = [
    [f"@color:red{{item {r}}}", f"@color:blue+bold{{{r * 10}}}", f"desc {r}"]
    for r in range(10)
]


def test_table_render_small(benchmark):
    """Render a 5×3 table (small, typical use case)."""
    response = TablePromptResponse.create_table(
        data=_SMALL_TABLE_DATA,
        headers=["Name", "Value", "Info"],
    )
    benchmark(response.render, CTX_WIDE)


def test_table_render_large(benchmark):
    """Render a 20×8 table; stresses column width calculation + row formatting."""
    response = TablePromptResponse.create_table(
        data=_LARGE_TABLE_DATA,
        headers=[f"Col{c}" for c in range(8)],
        title="Large Table",
    )
    benchmark(response.render, CTX_WIDE)


def test_table_render_styled_cells(benchmark):
    """Render a table where cells contain inline markup; exercises flatten_style_markup per cell."""
    response = TablePromptResponse.create_table(
        data=_STYLED_TABLE_DATA,
        headers=["Name", "Score", "Description"],
    )
    benchmark(response.render, CTX_WIDE)


def test_table_calculate_max_widths(benchmark):
    """Benchmark the column-width computation step in isolation."""
    benchmark(TablePromptResponse._calculate_max_widths, _LARGE_TABLE_DATA)
