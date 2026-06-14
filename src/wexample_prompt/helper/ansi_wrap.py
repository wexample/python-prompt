"""ANSI-aware word wrap that preserves SGR style continuity across breaks.

`textwrap.wrap` measures width with `len()` and is blind to ANSI escape
sequences — it counts them as visible chars (so the wrap math is wrong)
and it cheerfully breaks in the middle of an open style span, leaving
the terminal to apply the still-open SGR to whatever the caller adds
after the slice (padding spaces, box borders, the rest of the screen).

This helper:

- measures width with `terminal_get_visible_width` so emojis / CJK / OSC
  sequences are accounted for honestly;
- closes any open SGR at end-of-line with ``\\x1b[0m`` and re-emits the
  still-open openers at start of the next line — so paddings and
  borders downstream stay neutral;
- hard-splits a word that is itself wider than ``width`` (URLs, long
  identifiers) instead of overflowing.

Hyperlink OSC 8 sequences (``\\x1b]8;;url\\x1b\\\\label\\x1b]8;;\\x1b\\\\``)
are NOT split across lines today; if the label happens to span a wrap
boundary, the link will silently break across two lines. Rare enough
in practice to defer; can be addressed by tracking link open/close in
the same loop as SGR if it becomes a real problem.
"""

from __future__ import annotations

import re

_SGR_RE = re.compile(r"\x1b\[([0-9;]*)m")

# Map SGR closer param → opener params it cancels.
_SGR_CLOSERS: dict[str, frozenset[str]] = {
    "22": frozenset({"1", "2"}),  # bold + dim
    "23": frozenset({"3"}),  # italic
    "24": frozenset({"4"}),  # underline
    "27": frozenset({"7"}),  # reverse
    "29": frozenset({"9"}),  # strikethrough
    "39": frozenset(str(i) for i in (*range(30, 38), *range(90, 98))),  # default fg
    "49": frozenset(str(i) for i in (*range(40, 48), *range(100, 108))),  # default bg
}


def ansi_aware_wrap(text: str, width: int) -> list[str]:
    """Word-wrap ``text`` by visible width with ANSI style continuity.

    Returns a list of wrapped lines (one per visual row). Each line is
    self-contained for styling: it opens the styles it inherits from the
    previous line and closes anything still open at its end with
    ``\\x1b[0m`` — so a caller can safely concatenate borders or padding
    around each line without bleeding.
    """
    from wexample_prompt.helper.terminal import terminal_get_visible_width

    if width <= 0:
        return [text]
    if not text:
        return [""]

    # 1) Tokenize: ("sgr", raw, params) | ("char", ch) | ("space", ch).
    tokens: list[tuple] = []
    i = 0
    n = len(text)
    while i < n:
        m = _SGR_RE.match(text, i)
        if m:
            tokens.append(("sgr", m.group(0), m.group(1)))
            i = m.end()
            continue
        ch = text[i]
        tokens.append(("space" if ch == " " else "char", ch))
        i += 1

    # 2) Group into atoms separated by spaces. Spaces are their own atom.
    atoms: list[list[tuple]] = []
    word: list[tuple] = []
    for tok in tokens:
        if tok[0] == "space":
            if word:
                atoms.append(word)
                word = []
            atoms.append([tok])
        else:
            word.append(tok)
    if word:
        atoms.append(word)

    def atom_text(atom: list[tuple]) -> str:
        return "".join(t[1] for t in atom)

    def atom_update(atom: list[tuple], state: list[str]) -> list[str]:
        s = state
        for t in atom:
            if t[0] == "sgr":
                s = _apply_sgr(s, t[2])
        return s

    def hard_split(atom: list[tuple], cap: int) -> list[list[tuple]]:
        """Split a single oversize word into sub-atoms ≤ ``cap`` visible cols."""
        chunks: list[list[tuple]] = []
        current: list[tuple] = []
        current_w = 0
        for t in atom:
            if t[0] == "sgr":
                current.append(t)
                continue
            ch_w = terminal_get_visible_width(t[1])
            if current_w + ch_w > cap and current:
                chunks.append(current)
                current = []
                current_w = 0
            current.append(t)
            current_w += ch_w
        if current:
            chunks.append(current)
        return chunks

    # 3) Greedy wrap.
    lines: list[str] = []
    line_chunks: list[str] = []
    line_visible = 0
    active_state: list[str] = []  # SGR opener stack right now
    line_start_state: list[str] = []  # SGR opener stack at start of current line

    def flush_line() -> None:
        nonlocal line_chunks, line_visible, line_start_state
        prefix = _emit_sgr(line_start_state)
        suffix = "\x1b[0m" if active_state else ""
        lines.append(prefix + "".join(line_chunks) + suffix)
        line_chunks = []
        line_visible = 0
        line_start_state = list(active_state)

    for atom in atoms:
        raw = atom_text(atom)
        atom_w = terminal_get_visible_width(raw)
        is_space = atom[0][0] == "space"

        if is_space:
            # SGRs can ride in space atoms too in theory, but the tokenizer
            # puts SGRs in word atoms only — so a space atom is exactly one
            # whitespace char with no state effect.
            if line_visible == 0:
                # Skip leading space at start of a line.
                continue
            if line_visible + atom_w > width:
                # End-of-line trailing space: drop it, flush.
                flush_line()
                continue
            line_chunks.append(raw)
            line_visible += atom_w
            continue

        # Word atom — may include SGR codes.
        if line_visible + atom_w <= width:
            line_chunks.append(raw)
            line_visible += atom_w
            active_state = atom_update(atom, active_state)
            continue

        if atom_w <= width:
            # Whole word fits on a new line — flush current then place.
            if line_visible > 0:
                flush_line()
            line_chunks.append(raw)
            line_visible += atom_w
            active_state = atom_update(atom, active_state)
            continue

        # Word longer than width: hard-split, then drain pieces onto lines.
        for sub in hard_split(atom, width):
            sub_w = sum(terminal_get_visible_width(t[1]) for t in sub if t[0] != "sgr")
            if line_visible + sub_w > width and line_visible > 0:
                flush_line()
            line_chunks.append(atom_text(sub))
            line_visible += sub_w
            active_state = atom_update(sub, active_state)

    if line_chunks:
        flush_line()

    return lines or [""]


def _apply_sgr(active: list[str], params: str) -> list[str]:
    """Fold an SGR escape's params into the running opener stack."""
    parts = [p for p in params.split(";") if p]
    if not parts or parts == ["0"]:
        return []
    out = list(active)
    for p in parts:
        if p == "0":
            out = []
        elif p in _SGR_CLOSERS:
            cancel = _SGR_CLOSERS[p]
            out = [a for a in out if a not in cancel]
        else:
            out.append(p)
    return out


def _emit_sgr(active: list[str]) -> str:
    return f"\x1b[{';'.join(active)}m" if active else ""
