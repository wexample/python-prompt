"""Lightweight markdown -> ANSI/OSC8 renderer for terminal output.

Covers the realistic-for-CLI subset: headings, blockquotes, bullet and
numbered lists, fenced and inline code, bold/italic, links, images
(rendered as a labelled placeholder), and horizontal rules. Not a full
markdown engine — block nesting is flat and inline markup doesn't nest
across more than one level. Designed for short text snippets (issue
bodies, command descriptions, README excerpts) shown inside Properties,
Table cells, or message blocks.

The output stays compatible with `terminal_get_visible_width`: ANSI/OSC
sequences are stripped before width math, so the result can be fed to
the existing wrap/pad code without further care.
"""

from __future__ import annotations

import re

_RE_IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+[^)]*)?\)")
_RE_LINK = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)(?:\s+[^)]*)?\)")
_RE_CODE = re.compile(r"`([^`\n]+)`")
_RE_BOLD = re.compile(r"\*\*([^*\n]+)\*\*")
_RE_ITALIC = re.compile(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])")
_RE_BOLD_UNDERSCORE = re.compile(r"__([^_\n]+)__")
_RE_ITALIC_UNDERSCORE = re.compile(r"(?<!\w)_([^_\n]+)_(?!\w)")
_RE_STRIKE = re.compile(r"~~([^~\n]+)~~")

_RE_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
_RE_BLOCKQUOTE = re.compile(r"^>\s?(.*)$")
_RE_BULLET = re.compile(r"^(\s*)[-*+]\s+(.+)$")
_RE_NUMBERED = re.compile(r"^(\s*)(\d+)\.\s+(.+)$")
_RE_HR = re.compile(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$")
_RE_FENCE = re.compile(r"^\s*```")

_BOLD = ("\x1b[1m", "\x1b[22m")
_ITALIC = ("\x1b[3m", "\x1b[23m")
_DIM = ("\x1b[2m", "\x1b[22m")
_UNDERLINE = ("\x1b[4m", "\x1b[24m")
_STRIKE = ("\x1b[9m", "\x1b[29m")
_REVERSE = ("\x1b[7m", "\x1b[27m")

_HEADING_BULLETS = ("█", "▓", "▒", "░", "·", "·")


def markdown_to_ansi(text: str, *, hr_width: int = 40) -> str:
    """Render markdown-flavored ``text`` to ANSI/OSC8 terminal output.

    Args:
        text: source markdown.
        hr_width: visible width used for horizontal rules (``---``).
    """
    if not text:
        return ""

    lines = text.split("\n")
    out: list[str] = []
    in_code = False

    for raw in lines:
        if _RE_FENCE.match(raw):
            in_code = not in_code
            continue

        if in_code:
            out.append(f"  {_DIM[0]}{raw}{_DIM[1]}")
            continue

        if _RE_HR.match(raw):
            out.append(f"{_DIM[0]}{'─' * hr_width}{_DIM[1]}")
            continue

        m = _RE_HEADING.match(raw)
        if m:
            level = len(m.group(1))
            marker = _HEADING_BULLETS[min(level, len(_HEADING_BULLETS)) - 1]
            label = _render_inline(m.group(2))
            if level == 1:
                out.append(f"{_BOLD[0]}{_UNDERLINE[0]}{marker} {label}{_UNDERLINE[1]}{_BOLD[1]}")
            elif level == 2:
                out.append(f"{_BOLD[0]}{marker} {label}{_BOLD[1]}")
            else:
                out.append(f"{_DIM[0]}{marker} {_BOLD[0]}{label}{_BOLD[1]}{_DIM[1]}")
            continue

        m = _RE_BLOCKQUOTE.match(raw)
        if m:
            inner = _render_inline(m.group(1))
            out.append(f"{_DIM[0]}│{_DIM[1]} {inner}")
            continue

        m = _RE_BULLET.match(raw)
        if m:
            indent, body = m.group(1), m.group(2)
            out.append(f"{indent}{_DIM[0]}•{_DIM[1]} {_render_inline(body)}")
            continue

        m = _RE_NUMBERED.match(raw)
        if m:
            indent, num, body = m.group(1), m.group(2), m.group(3)
            out.append(f"{indent}{_DIM[0]}{num}.{_DIM[1]} {_render_inline(body)}")
            continue

        out.append(_render_inline(raw))

    return "\n".join(out)


def _render_inline(line: str) -> str:
    # Images first — they look like links but should NOT become hyperlinks
    # (the terminal can't render the image; fall back to a label).
    line = _RE_IMAGE.sub(_image_sub, line)
    # Links → OSC 8 hyperlink + underline (graceful fallback in dumb terms).
    line = _RE_LINK.sub(_link_sub, line)
    # Inline code: reverse video, tight spacing.
    line = _RE_CODE.sub(lambda m: f"{_REVERSE[0]} {m.group(1)} {_REVERSE[1]}", line)
    # Order matters: bold before italic so `**x**` isn't eaten by `*x*`.
    line = _RE_BOLD.sub(lambda m: f"{_BOLD[0]}{m.group(1)}{_BOLD[1]}", line)
    line = _RE_BOLD_UNDERSCORE.sub(lambda m: f"{_BOLD[0]}{m.group(1)}{_BOLD[1]}", line)
    line = _RE_ITALIC.sub(lambda m: f"{_ITALIC[0]}{m.group(1)}{_ITALIC[1]}", line)
    line = _RE_ITALIC_UNDERSCORE.sub(
        lambda m: f"{_ITALIC[0]}{m.group(1)}{_ITALIC[1]}", line
    )
    line = _RE_STRIKE.sub(lambda m: f"{_STRIKE[0]}{m.group(1)}{_STRIKE[1]}", line)
    return line


def _image_sub(m: re.Match[str]) -> str:
    alt = m.group(1).strip()
    url = m.group(2).strip()
    label = alt or url
    return f"{_DIM[0]}[image: {label}]{_DIM[1]}"


def _link_sub(m: re.Match[str]) -> str:
    label_md = m.group(1)
    url = m.group(2).strip()
    # Render inline styles inside the label too (bold/italic links exist).
    label = _RE_CODE.sub(
        lambda mm: f"{_REVERSE[0]} {mm.group(1)} {_REVERSE[1]}", label_md
    )
    label = _RE_BOLD.sub(lambda mm: f"{_BOLD[0]}{mm.group(1)}{_BOLD[1]}", label)
    label = _RE_ITALIC.sub(lambda mm: f"{_ITALIC[0]}{mm.group(1)}{_ITALIC[1]}", label)
    # OSC 8 hyperlink + underline fallback for terminals that ignore OSC 8.
    return f"\x1b]8;;{url}\x1b\\{_UNDERLINE[0]}{label}{_UNDERLINE[1]}\x1b]8;;\x1b\\"
