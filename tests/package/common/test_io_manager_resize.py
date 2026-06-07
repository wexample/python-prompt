"""Tests for IoManager's SIGWINCH dispatcher (subscribe_resize)."""

from __future__ import annotations


def test_enable_resize_listening_installs_the_handler() -> None:
    io = _make_io()
    installed = io.enable_resize_listening()
    assert installed is True
    assert io._winch_installed is True
    # Idempotent: a second call is a no-op.
    assert io.enable_resize_listening() is True


def test_listening_is_opt_in() -> None:
    """A fresh IoManager does NOT hijack the global SIGWINCH handler."""
    io = _make_io()
    assert io._winch_installed is False


def test_subscribe_returns_callable_unsubscribe() -> None:
    io = _make_io()
    fired = []

    unsubscribe = io.subscribe_resize(lambda: fired.append("called"))

    assert callable(unsubscribe)


def test_subscriber_exception_does_not_break_others() -> None:
    """A buggy subscriber must not silence its peers."""
    io = _make_io()
    fired = []

    def broken() -> None:
        raise RuntimeError("boom")

    io.subscribe_resize(broken)
    io.subscribe_resize(lambda: fired.append("ok"))

    io._on_sigwinch(28, None)

    assert fired == ["ok"]


def test_subscriber_is_invoked_on_winch() -> None:
    io = _make_io()
    fired = []
    io.subscribe_resize(lambda: fired.append("called"))

    # Simulate the signal handler firing (we can't reliably raise SIGWINCH
    # in CI / pytest; calling the bound handler directly is equivalent).
    io._on_sigwinch(28, None)

    assert fired == ["called"]


def test_unsubscribed_callback_no_longer_fires() -> None:
    io = _make_io()
    fired = []
    unsubscribe = io.subscribe_resize(lambda: fired.append("called"))

    unsubscribe()
    io._on_sigwinch(28, None)

    assert fired == []


def test_winch_refreshes_width_cache_before_callbacks() -> None:
    """Subscribers can read `terminal_width` synchronously and get fresh data."""
    io = _make_io()
    seen_at_callback: list[int] = []

    def callback() -> None:
        seen_at_callback.append(io._terminal_width)

    io.subscribe_resize(callback)
    # Stale value before the signal.
    io._terminal_width = -1

    io._on_sigwinch(28, None)

    # Cache was refreshed before the callback fired (so it's a real,
    # positive column count, not the -1 we put there).
    assert seen_at_callback
    assert seen_at_callback[0] > 0


def _make_io() -> IoManager:
    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.output.prompt_buffer_output_handler import (
        PromptBufferOutputHandler,
    )

    # The dispatcher itself works without a real SIGWINCH installation;
    # we call `_on_sigwinch` manually below. Leaving the listener
    # disabled also avoids tests fighting for the real signal handler.
    return IoManager(output=PromptBufferOutputHandler())
