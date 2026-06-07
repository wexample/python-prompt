"""Unit tests for the InputWidget keystroke parser (_try_extract_key).

The parser is a pure function over a byte buffer: it turns raw tty
input into one logical key at a time (plain char, Alt+X, CSI/SS3,
bracketed paste) or returns (None, 0) when more bytes are needed.

These tests poke it in isolation — no real stdin, no timing magic,
just hand-crafted inputs. Real-terminal quirks are tested separately
once we encounter them.
"""

from __future__ import annotations


def test_alt_enter_two_bytes() -> None:
    """`\\x1b\\r` (Alt+Enter / Esc+Enter) is a 2-byte logical key."""
    widget = _new_widget()

    key, consumed = widget._try_extract_key(
        buf="\x1b\r", esc_seq_started_at=0.0, now=0.001, budget=5.0
    )

    assert key == "\x1b\r"
    assert consumed == 2


def test_arrow_down_complete() -> None:
    """A complete `\\x1b[B` (Down) arrives in one buffer — should dispatch."""
    widget = _new_widget()

    key, consumed = widget._try_extract_key(
        buf="\x1b[B",
        esc_seq_started_at=0.0,
        now=0.001,
        budget=5.0,
    )

    assert key == "\x1b[B"
    assert consumed == 3


def test_bare_esc_waits_then_drops() -> None:
    """A lone `\\x1b` waits while inside the budget, drops once it expires."""
    widget = _new_widget()

    # Inside budget: wait.
    key, consumed = widget._try_extract_key(
        buf="\x1b", esc_seq_started_at=0.0, now=0.1, budget=5.0
    )
    assert key is None
    assert consumed == 0

    # Past budget: drop silently (Escape has no action in this widget).
    key, consumed = widget._try_extract_key(
        buf="\x1b", esc_seq_started_at=0.0, now=10.0, budget=5.0
    )
    assert key == "__DROP__"
    assert consumed == 1


def test_bracketed_paste_complete() -> None:
    """Paste delimited by `\\x1b[200~` … `\\x1b[201~` returns its inner text."""
    widget = _new_widget()

    buf = "\x1b[200~hello world\x1b[201~"
    key, consumed = widget._try_extract_key(
        buf=buf, esc_seq_started_at=0.0, now=0.1, budget=5.0
    )

    assert key == ("PASTE", "hello world")
    assert consumed == len(buf)


def test_bracketed_paste_incomplete_waits() -> None:
    """Paste without its end marker yet → wait."""
    widget = _new_widget()

    key, consumed = widget._try_extract_key(
        buf="\x1b[200~hello",
        esc_seq_started_at=0.0,
        now=0.1,
        budget=5.0,
    )

    assert key is None
    assert consumed == 0


def test_buffer_with_trailing_extra_only_consumes_one_key() -> None:
    """A complete key followed by extra bytes consumes only the key itself."""
    widget = _new_widget()

    key, consumed = widget._try_extract_key(
        buf="\x1b[B\x1b",
        esc_seq_started_at=0.0,
        now=0.1,
        budget=5.0,
    )

    assert key == "\x1b[B"
    assert consumed == 3


def test_csi_incomplete_waits() -> None:
    """`\\x1b[` without a final byte inside the budget → wait."""
    widget = _new_widget()

    key, consumed = widget._try_extract_key(
        buf="\x1b[",
        esc_seq_started_at=0.0,
        now=0.1,
        budget=5.0,
    )

    assert key is None
    assert consumed == 0


def test_plain_printable_char_a() -> None:
    """A single printable byte returns itself as a 1-char key."""
    widget = _new_widget()

    key, consumed = widget._try_extract_key(
        buf="a",
        esc_seq_started_at=None,
        now=0.0,
        budget=5.0,
    )

    assert key == "a"
    assert consumed == 1


def _new_widget() -> InputWidget:
    """Fresh widget instance, just to call the parser method on."""
    from wexample_prompt.helper.input_widget import InputWidget

    return InputWidget(bordered=False, width=80)
