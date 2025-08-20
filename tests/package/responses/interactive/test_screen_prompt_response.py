"""Tests for ScreenPromptResponse (interactive)."""

from typing import Callable

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.testing.abstract_prompt_response_test import (
    AbstractPromptResponseTest,
)


class TestScreenPromptResponse(AbstractPromptResponseTest):
    """Focused tests for ScreenPromptResponse core behavior with callback."""

    def create_test_response(self, **kwargs) -> AbstractPromptResponse:
        from wexample_prompt.responses.interactive.screen_prompt_response import (
            ScreenPromptResponse,
        )

        # Minimal callback: draw one line and close immediately
        def _cb_once(resp: "ScreenPromptResponse"):
            resp.clear()
            resp.print(self._test_message)
            resp.close()

        kwargs.setdefault("callback", _cb_once)
        kwargs.setdefault("height", 5)
        return ScreenPromptResponse.create_screen(**kwargs)

    def _assert_specific_format(self, rendered: str):
        # Should simply contain our message (single line screen)
        self._assert_contains_text(rendered, self._test_message)

    def get_expected_lines(self) -> int:
        # One printed line
        return 1

    # Override to match single-line behavior (no implicit empty line)
    def _assert_common_response_structure(self, response: "AbstractPromptResponse"):
        lines = response.rendered_content.split("\n")
        assert len(lines) == self.get_expected_lines()
        self._assert_contains_text(lines[0], self._test_message)

    def test_single_frame_close(self):
        response = self.create_test_response()
        response.render()
        # After render, last frame is stored in rendered_content
        self._assert_contains_text(response.rendered_content, self._test_message)

    def test_reload_then_close(self):
        from wexample_prompt.responses.interactive.screen_prompt_response import ScreenPromptResponse

        ticks = {"n": 0}

        def _cb(resp: ScreenPromptResponse):
            resp.clear()
            resp.print(f"tick {ticks['n']}")
            if ticks["n"] < 2:
                ticks["n"] += 1
                resp.reload()
            else:
                resp.close()

        response = self.create_test_response(callback=_cb)
        response.render()
        # Final frame should reflect the last tick (2)
        self._assert_contains_text(response.rendered_content, "tick 2")

    def test_manager_entrypoint(self):
        # Ensure IoManager.screen constructs and renders without error
        from wexample_prompt.responses.interactive.screen_prompt_response import ScreenPromptResponse

        steps = {"n": 0}

        def _cb(resp: ScreenPromptResponse):
            resp.clear()
            resp.print(f"step {steps['n']}")
            steps["n"] += 1
            if steps["n"] >= 1:
                resp.close()
            else:
                resp.reload()

        response = self._io.screen(callback=_cb, height=3)
        assert isinstance(response, AbstractPromptResponse)
        # rendered_content available after render via StdoutOutputHandler
        self._assert_contains_text(response.rendered_content, "step 0")

    def test_reset_on_finish_triggers_clear(self):
        """When reset_on_finish=True, Screen should perform a final clear after closing."""
        from wexample_prompt.responses.interactive.screen_prompt_response import ScreenPromptResponse

        clears = {"count": 0, "last": None}

        def _cb(resp: ScreenPromptResponse):
            # Draw two lines then request close on first pass
            resp.clear()
            resp.print("line A")
            resp.print("line B")
            if clears["count"] == 0:
                # ask to close so that a final clear should occur
                resp.close()
            else:
                resp.reload()

        resp = self.create_test_response(callback=_cb, reset_on_finish=True)

        # Monkeypatch _partial_clear to observe calls
        original_clear = resp._partial_clear

        def _spy(lines):
            clears["count"] += 1
            clears["last"] = lines
            try:
                original_clear(lines)
            except Exception:
                pass

        setattr(resp, "_partial_clear", _spy)

        resp.render()

        # Expect that clear was called at least once, and last cleared lines > 0 (clearing printed block)
        assert clears["count"] >= 1
        assert isinstance(clears["last"], int) and clears["last"] > 0
