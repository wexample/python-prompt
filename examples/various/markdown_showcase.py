"""Visual showcase of `markdown_to_ansi` over every common markdown feature.

Run directly:

    python examples/various/markdown_showcase.py

Each section prints: a label, a "supported / fallback" badge, the raw
markdown source, and the rendered ANSI output. Features the helper
recognizes render as expected; features it doesn't fall through as
plain text — both behaviors are demonstrated here so the gap is
visible at a glance instead of being guessed from the source.
"""

from __future__ import annotations

from wexample_prompt.helper.markdown import markdown_to_ansi

_DIM = "\x1b[2m"
_BOLD = "\x1b[1m"
_GREEN = "\x1b[32m"
_YELLOW = "\x1b[33m"
_RESET = "\x1b[0m"

# (label, supported, markdown_source). `supported=True` means the helper has
# a dedicated rule for this construct; `False` means it falls through as raw
# text (or as the closest supported construct — e.g. `- [x]` becomes a
# regular bullet because checkbox syntax isn't recognized).
SECTIONS: list[tuple[str, bool, str]] = [
    # ---- Inline ----------------------------------------------------------
    ("Bold (stars)", True, "**hello world**"),
    ("Bold (underscores)", True, "__hello world__"),
    ("Italic (stars)", True, "*hello world*"),
    ("Italic (underscores)", True, "_hello world_"),
    ("Strikethrough", True, "~~deprecated~~"),
    ("Inline code", True, "Run `pytest -v` to verify."),
    ("Link", True, "See [the docs](https://example.com) for more."),
    ("Image", True, "![Logo](https://example.com/logo.png)"),
    ("Autolink", False, "Visit <https://example.com> directly."),
    (
        "Reference-style link",
        False,
        "See [the docs][docs].\n\n[docs]: https://example.com",
    ),
    ("Escaped emphasis", False, "Literal \\*stars\\* should not bold."),
    ("Nested emphasis", False, "**bold _and italic_ inside**"),
    # ---- Headings --------------------------------------------------------
    ("Heading H1", True, "# Heading One"),
    ("Heading H2", True, "## Heading Two"),
    ("Heading H3", True, "### Heading Three"),
    ("Headings H4 / H5 / H6", True, "#### H4\n##### H5\n###### H6"),
    ("Setext H1 (===)", False, "Heading One\n==========="),
    ("Setext H2 (---)", False, "Heading Two\n-----------"),
    # ---- Quotes / lists --------------------------------------------------
    ("Blockquote", True, "> Stay focused on the task."),
    ("Multi-line blockquote", True, "> first line\n> second line"),
    ("Nested blockquote", False, "> outer\n>> inner"),
    ("Bullet list (-)", True, "- alpha\n- beta\n- gamma"),
    ("Bullet list (*)", True, "* alpha\n* beta"),
    ("Bullet list (+)", True, "+ alpha\n+ beta"),
    ("Numbered list", True, "1. first\n2. second\n3. third"),
    ("Nested list", False, "- outer\n  - inner\n  - inner two\n- next"),
    ("Task list", False, "- [ ] todo\n- [x] done"),
    ("Definition list", False, "Term\n: Definition of the term"),
    # ---- Code / rules / tables ------------------------------------------
    ("Fenced code block", True, "```\ndef hi():\n    return 1\n```"),
    (
        "Fenced code with language tag",
        False,
        "```python\ndef hi():\n    return 1\n```",
    ),
    ("Indented code (4 spaces)", False, "    indented code line"),
    ("Horizontal rule (---)", True, "---"),
    ("Horizontal rule (***)", True, "***"),
    ("Horizontal rule (___)", True, "___"),
    (
        "Table",
        False,
        "| col A | col B |\n| ----- | ----- |\n| 1     | 2     |",
    ),
    ("Footnote", False, "See note[^1].\n\n[^1]: Footnote body."),
    ("HTML tags", False, "<strong>not parsed</strong>"),
    # ---- Realistic mix ---------------------------------------------------
    (
        "Realistic mix (release notes)",
        True,
        (
            "## Release notes — v1.4\n"
            "\n"
            "**Highlights**:\n"
            "\n"
            "- Wrapped properties values\n"
            "- New `io.leader_line(...)` helper — see "
            "[the docs](https://example.com)\n"
            "\n"
            "> Heads up: the cyan `io.command` is now dim grey.\n"
            "\n"
            "---\n"
            "\n"
            "```\n"
            "io.leader_line('Build').get_handle().success()\n"
            "```"
        ),
    ),
]


def _print_section(label: str, supported: bool, source: str) -> None:
    badge = (
        f"{_BOLD}{_GREEN}✓ supported{_RESET}"
        if supported
        else f"{_BOLD}{_YELLOW}✗ fallback{_RESET}"
    )
    print(f"\n{_BOLD}── {label}{_RESET}   {badge}")
    print(f"{_DIM}source:{_RESET}")
    for line in source.split("\n"):
        print(f"{_DIM}│{_RESET} {line}")
    print(f"{_DIM}rendered:{_RESET}")
    for line in markdown_to_ansi(source).split("\n"):
        print(f"{_DIM}│{_RESET} {line}")


def main() -> None:
    print(f"{_BOLD}markdown_to_ansi — visual showcase{_RESET}")
    print(
        f"{_DIM}supported = the helper has a dedicated rule. "
        f"fallback = the source falls through as plain text "
        f"(or to the nearest supported rule).{_RESET}"
    )
    for label, supported, source in SECTIONS:
        _print_section(label, supported, source)


if __name__ == "__main__":
    main()
