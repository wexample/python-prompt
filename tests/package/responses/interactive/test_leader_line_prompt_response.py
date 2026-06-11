"""Tests for LeaderLinePromptResponse and its handle."""

from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.helpers.ansi import ansi_strip

from wexample_prompt.testing.abstract_prompt_response_test import (
    AbstractPromptResponseTest,
)

if TYPE_CHECKING:
    from wexample_helpers.const.types import Kwargs

    from wexample_prompt.responses.abstract_prompt_response import (
        AbstractPromptResponse,
    )


class TestLeaderLinePromptResponse(AbstractPromptResponseTest):
    __test__ = True

    def get_expected_lines(self) -> int:
        return 1

    def test_custom_markers_bundle(self) -> None:
        from wexample_prompt.common.leader.leader_markers import (
            LeaderLineMarkers,
            StatusMarker,
        )
        from wexample_prompt.responses.interactive.leader_line_prompt_response import (
            LeaderLinePromptResponse,
        )

        markers = LeaderLineMarkers(
            pending=StatusMarker(label="?"),
            success=StatusMarker(label="DONE"),
            failure=StatusMarker(label="ABORT"),
        )
        resp = LeaderLinePromptResponse.create_leader_line(
            message="Task", state="success", markers=markers
        )
        rendered = ansi_strip(resp.render() or "")
        assert "DONE" in rendered

    def test_dots_fill_available_width(self) -> None:
        """With a fixed width, the dot leader stretches to reach the marker."""
        from wexample_prompt.responses.interactive.leader_line_prompt_response import (
            LeaderLinePromptResponse,
        )

        resp = LeaderLinePromptResponse.create_leader_line(
            message="a", state="success", width=40
        )
        rendered = ansi_strip(resp.render() or "")
        assert rendered.count(".") >= 30  # plenty of dots between "a" and "✓"

    def test_failure_state_with_status_appears_after_marker(self) -> None:
        from wexample_prompt.responses.interactive.leader_line_prompt_response import (
            LeaderLinePromptResponse,
        )

        resp = LeaderLinePromptResponse.create_leader_line(
            message="Connect", state="failure", status="timeout"
        )
        rendered = ansi_strip(resp.render() or "")
        assert "✗" in rendered
        assert "timeout" in rendered
        # The status sits after the marker, not before it.
        assert rendered.index("✗") < rendered.index("timeout")

    def test_handle_failure_sets_status_text(self) -> None:
        from wexample_prompt.responses.interactive.leader_line_prompt_response import (
            LeaderLinePromptResponse,
        )

        resp = LeaderLinePromptResponse.create_leader_line(message="x")
        resp.init_handle()
        handle = resp.get_handle()
        handle.failure(status="boom", auto_render=False)
        assert resp.state == "failure"
        assert resp.status == "boom"

    def test_handle_render_emits_in_place_escape_sequence(self) -> None:
        """A re-render must climb one row and clear the line so the previous
        frame is overwritten in place — same trick as the progress widget."""
        from wexample_prompt.responses.interactive.leader_line_prompt_response import (
            LeaderLinePromptResponse,
        )

        resp = LeaderLinePromptResponse.create_leader_line(message="x")
        resp.init_handle()
        first = resp.render() or ""
        # First render: no in-place prefix (this is the initial paint).
        assert not first.startswith("\x1b[1A")
        # Handle re-render: must climb and erase.
        re_rendered = resp.get_handle().success() or ""
        assert re_rendered.startswith("\x1b[1A\x1b[2K\r")

    def test_handle_success_updates_state(self) -> None:
        from wexample_prompt.responses.interactive.leader_line_prompt_response import (
            LeaderLinePromptResponse,
        )

        resp = LeaderLinePromptResponse.create_leader_line(message="x")
        resp.init_handle()
        handle = resp.get_handle()
        handle.success(auto_render=False)
        assert resp.state == "success"

    def test_marker_bundle_rejects_missing_state(self) -> None:
        import pytest

        from wexample_prompt.common.leader.leader_markers import (
            LeaderLineMarkers,
            StatusMarker,
        )

        markers = LeaderLineMarkers(
            pending=StatusMarker(label="?"),
            success=StatusMarker(label="ok"),
            failure=StatusMarker(label="ko"),
        )
        with pytest.raises(ValueError, match="warning"):
            markers.get("warning")

    def test_ok_ko_preset_uses_bracketed_markers(self) -> None:
        from wexample_prompt.responses.interactive.leader_line_prompt_response import (
            LeaderLinePromptResponse,
        )

        resp = LeaderLinePromptResponse.create_leader_line(
            message="Test",
            state="success",
            markers=LeaderLinePromptResponse.MARKERS_PRESET_OK_KO,
        )
        rendered = ansi_strip(resp.render() or "")
        assert "[OK]" in rendered
        assert "✓" not in rendered

    def test_pass_fail_preset(self) -> None:
        from wexample_prompt.responses.interactive.leader_line_prompt_response import (
            LeaderLinePromptResponse,
        )

        resp = LeaderLinePromptResponse.create_leader_line(
            message="test_x",
            state="failure",
            markers=LeaderLinePromptResponse.MARKERS_PRESET_PASS_FAIL,
        )
        rendered = ansi_strip(resp.render() or "")
        assert "FAIL" in rendered

    def test_pending_state_renders_pending_marker(self) -> None:
        from wexample_prompt.responses.interactive.leader_line_prompt_response import (
            LeaderLinePromptResponse,
        )

        resp = LeaderLinePromptResponse.create_leader_line(message="Migrating")
        rendered = ansi_strip(resp.render() or "")
        assert "Migrating" in rendered
        assert "…" in rendered
        assert "✓" not in rendered
        assert "✗" not in rendered

    def test_success_state_swaps_marker(self) -> None:
        from wexample_prompt.responses.interactive.leader_line_prompt_response import (
            LeaderLinePromptResponse,
        )

        resp = LeaderLinePromptResponse.create_leader_line(
            message="Build", state="success"
        )
        rendered = ansi_strip(resp.render() or "")
        assert "✓" in rendered
        assert "✗" not in rendered

    def _assert_specific_format(self, rendered: str) -> None:
        # Every leader line has a dot leader and a state marker.
        assert "." in rendered
        # Pending marker (default preset) — strip ANSI first.
        assert "…" in ansi_strip(rendered)

    def _create_test_kwargs(self, kwargs=None) -> Kwargs:
        kwargs = kwargs or {}
        kwargs.setdefault("message", self._test_message)
        return kwargs

    def _get_response_class(self) -> type[AbstractPromptResponse]:
        from wexample_prompt.responses.interactive.leader_line_prompt_response import (
            LeaderLinePromptResponse,
        )

        return LeaderLinePromptResponse
