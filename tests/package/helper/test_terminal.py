from __future__ import annotations

CSI_RED = "\x1b[31m"
CSI_RESET = "\x1b[0m"


def test_terminal_get_visible_width_ascii() -> None:
    from wexample_prompt.helper.terminal import terminal_get_visible_width

    assert terminal_get_visible_width("hello") == 5


def test_terminal_get_visible_width_counts_cjk_as_double() -> None:
    from wexample_prompt.helper.terminal import terminal_get_visible_width

    assert terminal_get_visible_width("中文") == 4


def test_terminal_get_visible_width_empty_string() -> None:
    from wexample_prompt.helper.terminal import terminal_get_visible_width

    assert terminal_get_visible_width("") == 0


def test_terminal_get_visible_width_ignores_sequences() -> None:
    from wexample_prompt.helper.terminal import terminal_get_visible_width

    assert terminal_get_visible_width(f"{CSI_RED}hello{CSI_RESET}") == 5


def test_terminal_get_visible_width_never_negative() -> None:
    from wexample_prompt.helper.terminal import terminal_get_visible_width

    assert terminal_get_visible_width("\x01\x02") >= 0


def test_terminal_strip_sequences_removes_csi() -> None:
    from wexample_prompt.helper.terminal import terminal_strip_sequences

    assert terminal_strip_sequences(f"{CSI_RED}hello{CSI_RESET}") == "hello"
