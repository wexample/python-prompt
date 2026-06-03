"""Sticky bottom-line spinner with live event logging above it."""

from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.responses.interactive.abstract_interactive_prompt_response import (
    AbstractInteractivePromptResponse,
)

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.example.abstract_response_example import (
        AbstractResponseExample,
    )


@base_class
class SpinnerPromptResponse(AbstractInteractivePromptResponse):
    """A spinner that stays at the bottom of the terminal flow.

    Unlike ``PendingPromptResponse`` (which owns a whole header+body block and
    rewrites it on each tick), this one only owns its own line. Calling
    ``.log(line)`` clears the spinner line, writes ``line`` as a persistent
    row, and the spinner re-draws below on the next tick. Same pattern as
    Claude Code / Cursor's tool-event feed.

    Typical usage::

        spinner = io.spinner(label="Thinking…")
        worker.start()
        while worker.is_alive():
            for event in drain_events():
                spinner.log(event)
            time.sleep(0.05)
        worker.join()
        spinner.stop()
    """

    interval: float = public_field(
        default=0.1,
        description="Seconds between spinner frame advances.",
    )
    label: str = public_field(
        default="Thinking…",
        description="Text shown next to the spinning glyph.",
    )

    @classmethod
    def create_spinner(
        cls,
        label: str = "Thinking…",
        interval: float = 0.1,
    ) -> SpinnerPromptResponse:
        return cls(label=label, interval=interval)

    @classmethod
    def get_example_class(cls) -> type[AbstractResponseExample]:
        from wexample_prompt.example.response.interactive.spinner_example import (
            SpinnerExample,
        )

        return SpinnerExample

    # ─── handle API ──────────────────────────────────────────────────────
    def log(self, line: str) -> None:
        """Print ``line`` as a persistent row above the spinner."""
        import sys

        if not getattr(self, "_running", False):
            return
        with self._lock:
            sys.stdout.write("\r\x1b[2K")
            sys.stdout.write(f"{line}\n")
            sys.stdout.flush()
            self._draw()

    def render(self, context: PromptContext | None = None) -> None:
        """Start the spinner thread; return immediately so the caller can act."""
        import threading

        from wexample_prompt.common.prompt_context import PromptContext
        from wexample_prompt.common.spinner_pool import Spinner

        context = PromptContext.create_if_none(context=context)
        if not self._verbosity_context_allows_display(context=context):
            return None

        # Instance state (set after attrs init — bypasses any unused field
        # ceremony and stays local to the live handle).
        self._spinner_inst = Spinner(interval=self.interval)
        self._lock = threading.Lock()
        self._running = True
        self._thread = threading.Thread(target=self._spin_loop, daemon=True)

        self._draw_locked = False  # guard against re-entry
        self._draw()
        self._thread.start()
        return None

    def stop(self) -> None:
        """Stop the spinner and erase its line."""
        import sys

        if not getattr(self, "_running", False):
            return
        self._running = False
        if self._thread is not None:
            self._thread.join(timeout=max(self.interval * 2, 0.2))
        with self._lock:
            sys.stdout.write("\r\x1b[2K")
            sys.stdout.flush()

    def _draw(self) -> None:
        import sys

        if not self._running:
            return
        frame = self._spinner_inst.next()
        sys.stdout.write(f"\r\x1b[2K{frame} {self.label}")
        sys.stdout.flush()

    # ─── internals ───────────────────────────────────────────────────────
    def _spin_loop(self) -> None:
        import time

        while self._running:
            time.sleep(self.interval)
            if not self._running:
                break
            with self._lock:
                if self._running:
                    self._draw()
