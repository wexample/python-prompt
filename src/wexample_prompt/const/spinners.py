"""Spinner frame presets for terminal UIs.

Note: Not all terminals render every Unicode glyph identically. Keep a few
ASCII-friendly presets as well. You can trim this list later.
"""
from __future__ import annotations

# filestate: python-constant-sort
# Braille-style spinner (smooth, compact, good Unicode support in modern terminals)
BRAILLE_SPINNER_FRAMES: list[str] = [
    "⣷",
    "⣯",
    "⣟",
    "⡿",
    "⢿",
    "⣻",
    "⣽",
    "⣾",
]
PIPE_SPINNER_FRAMES: list[str] = ["|", "/", "-", "\\"]
LINE_SPINNER_FRAMES: list[str] = ["-", "\\", "|", "/"]
DOTS_FRAMES: list[str] = ["․  ", "․․ ", "․․․", "   "]
DOTS_BOUNCE_FRAMES: list[str] = [".  ", ".. ", "...", " ..", "  .", "   "]
ELLIPSIS_FRAMES: list[str] = ["", ".", "..", "..."]
ARROW_FRAMES: list[str] = ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"]
ARROW_THIN_FRAMES: list[str] = ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"]
QUADRANT_FRAMES: list[str] = ["▖", "▘", "▝", "▗"]
BLOCK_SHADES_FRAMES: list[str] = ["░", "▒", "▓", "█", "▓", "▒"]
BAR_FRAMES: list[str] = [
    "▁",
    "▂",
    "▃",
    "▄",
    "▅",
    "▆",
    "▇",
    "█",
    "▇",
    "▆",
    "▅",
    "▄",
    "▃",
    "▂",
]
GROW_VERTICAL_FRAMES: list[str] = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
CLASSIC_CIRCLE_FRAMES: list[str] = ["◴", "◷", "◶", "◵"]
BOUNCE_FRAMES: list[str] = [
    "⠁",
    "⠂",
    "⠄",
    "⡀",
    "⢀",
    "⠠",
    "⠐",
    "⠈",
]
TOGGLE_FRAMES: list[str] = ["⊶", "⊷"]
TOGGLE_SQUARE_FRAMES: list[str] = ["▮", "▯"]
CLOCK_FRAMES: list[str] = [
    "🕛",
    "🕐",
    "🕑",
    "🕒",
    "🕓",
    "🕔",
    "🕕",
    "🕖",
    "🕗",
    "🕘",
    "🕙",
    "🕚",
]
TRIANGLE_FRAMES: list[str] = ["◢", "◣", "◤", "◥"]
SQUARE_FRAMES: list[str] = ["▖", "▘", "▝", "▗"]
CIRCLE_QUADRANT_FRAMES: list[str] = [
    "◐",
    "◓",
    "◑",
    "◒",
]
DOT_PULSE_FRAMES: list[str] = ["∙    ", "∙∙   ", "∙∙∙  ", "∙∙∙∙ ", "∙∙∙∙∙", "     "]
ASCII_WAVE_FRAMES: list[str] = ["_", "-", "^", "-", "_"]
DEFAULT_SPINNER_FRAMES: list[str] = BRAILLE_SPINNER_FRAMES
SPINNER_PRESETS: dict[str, list[str]] = {
    "default": DEFAULT_SPINNER_FRAMES,
    "braille": BRAILLE_SPINNER_FRAMES,
    "pipe": PIPE_SPINNER_FRAMES,
    "line": LINE_SPINNER_FRAMES,
    "dots": DOTS_FRAMES,
    "dots_bounce": DOTS_BOUNCE_FRAMES,
    "ellipsis": ELLIPSIS_FRAMES,
    "arrow": ARROW_FRAMES,
    "arrow_thin": ARROW_THIN_FRAMES,
    "quadrant": QUADRANT_FRAMES,
    "block_shades": BLOCK_SHADES_FRAMES,
    "bar": BAR_FRAMES,
    "grow_vertical": GROW_VERTICAL_FRAMES,
    "circle": CLASSIC_CIRCLE_FRAMES,
    "bounce": BOUNCE_FRAMES,
    "toggle": TOGGLE_FRAMES,
    "toggle_square": TOGGLE_SQUARE_FRAMES,
    "clock": CLOCK_FRAMES,
    "triangle": TRIANGLE_FRAMES,
    "square": SQUARE_FRAMES,
    "circle_dots": CIRCLE_QUADRANT_FRAMES,
    "dot_pulse": DOT_PULSE_FRAMES,
    "ascii_wave": ASCII_WAVE_FRAMES,
}
