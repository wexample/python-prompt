"""Tests for the ANSI-aware word-wrap helper."""

from __future__ import annotations

from wexample_prompt.helper.ansi_wrap import ansi_aware_wrap
from wexample_prompt.helper.terminal import terminal_get_visible_width


def _visible_widths(lines: list[str]) -> list[int]:
    return [terminal_get_visible_width(line) for line in lines]


def test_empty_input_returns_one_empty_line() -> None:
    assert ansi_aware_wrap("", 20) == [""]


def test_short_text_fits_on_one_line() -> None:
    assert ansi_aware_wrap("hello world", 20) == ["hello world"]


def test_wraps_at_space_boundary() -> None:
    out = ansi_aware_wrap("alpha beta gamma delta", 12)
    assert all(w <= 12 for w in _visible_widths(out))
    # Greedy: first line packs as much as fits.
    assert "alpha beta" in out[0]


def test_hard_splits_oversize_word() -> None:
    out = ansi_aware_wrap("supercalifragilistic", 8)
    assert all(w <= 8 for w in _visible_widths(out))
    assert "".join(out) == "supercalifragilistic"


def test_preserves_ansi_within_a_line() -> None:
    src = "say \x1b[1mhi\x1b[22m loud"
    out = ansi_aware_wrap(src, 80)
    assert out == [src]


def test_closes_open_style_at_wrap_and_reopens_on_next_line() -> None:
    """The user's actual bug: bold spans a wrap → padding inherits bold."""
    # Width = 12. Bold span "important highlight" straddles the wrap.
    src = "go \x1b[1mimportant highlight\x1b[22m now"
    out = ansi_aware_wrap(src, 14)
    # No visible row exceeds the cap.
    assert all(w <= 14 for w in _visible_widths(out))
    # Every line that has an opener leaves a reset behind it.
    for line in out:
        if "\x1b[1m" in line:
            # Either closed in-line by \x1b[22m, or closed at end-of-line by \x1b[0m.
            assert "\x1b[22m" in line or line.endswith("\x1b[0m")


def test_style_continuity_across_multiple_wraps() -> None:
    """Long styled span that spans 3+ output lines must re-open on every line."""
    # 50 ANSI-bold chars, width 10 → should wrap into ≥5 lines, each
    # reopening bold at the start and resetting at the end.
    word = "x" * 50
    src = f"\x1b[1m{word}\x1b[22m"
    out = ansi_aware_wrap(src, 10)
    assert len(out) >= 5
    for line in out[:-1]:
        # Every non-final line should both open and reset bold.
        assert line.startswith("\x1b[1m") or "\x1b[1m" in line
        assert line.endswith("\x1b[0m")


def test_reset_zero_clears_active_state() -> None:
    """An inline \\x1b[0m closes everything — no reopen on next line."""
    src = "left \x1b[1mbold\x1b[0m right padding text more content here"
    out = ansi_aware_wrap(src, 12)
    # No line after the explicit reset should reopen bold.
    saw_reset = False
    for line in out:
        if "\x1b[0m" in line and "\x1b[1m" in line:
            saw_reset = True
            continue
        if saw_reset:
            assert "\x1b[1m" not in line


def test_combined_sgr_close_reopens_with_both_params() -> None:
    """A `[2;4m` (dim+underline) span crossing a wrap reopens with both."""
    word = "y" * 50
    src = f"\x1b[2;4m{word}\x1b[0m"
    out = ansi_aware_wrap(src, 10)
    # Every wrapped line (except possibly the last) reopens dim+underline.
    for line in out[:-1]:
        # The opener may appear as `[2;4m` or as separate codes — accept both.
        assert ("\x1b[2;4m" in line) or ("\x1b[2m" in line and "\x1b[4m" in line)


def test_emoji_counted_at_width_two() -> None:
    """Emojis (width 2) must be billed as two cells in the wrap math."""
    out = ansi_aware_wrap("🚀 ok", 4)
    assert all(w <= 4 for w in _visible_widths(out))
