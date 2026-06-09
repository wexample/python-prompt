"""Leader-line response — movie-credits style status reporting.

Renders as ``{message} {dots…} {marker}{optional status}`` where the
dot leader stretches to fill the available terminal width. The state
(`pending`/`success`/`failure`/…) picks which marker to display via a
:class:`LeaderLineMarkers` bundle, with three built-in presets and full
control over a custom bundle for callers that want a different look.

Typical usage::

    handle = io.leader_line("Migrating database")
    # ... do the work ...
    handle.success()                       # ✓
    # or
    handle.failure("connection refused")   # ✗ connection refused
"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.common.leader.leader_markers import (
    LeaderLineMarkers,
    StatusMarker,
)
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.enums.text_style import TextStyle
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse

if TYPE_CHECKING:
    from wexample_prompt.common.leader.leader_line_handle import LeaderLineHandle
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.enums.verbosity_level import VerbosityLevel


_DIM = [TextStyle.DIM]
_BOLD = [TextStyle.BOLD]


@base_class
class LeaderLinePromptResponse(AbstractPromptResponse):
    """Single-line widget with a left message, dot leader, and a state marker."""

    DEFAULT_DOT_CHAR: ClassVar[str] = "."

    # --- Built-in presets ---------------------------------------------------
    MARKERS_PRESET_CHECK: ClassVar[LeaderLineMarkers] = LeaderLineMarkers(
        pending=StatusMarker(label="…", color=TerminalColor.LIGHT_BLACK, styles=_DIM),
        success=StatusMarker(label="✓", color=TerminalColor.GREEN, styles=_BOLD),
        failure=StatusMarker(label="✗", color=TerminalColor.RED, styles=_BOLD),
        warning=StatusMarker(label="!", color=TerminalColor.YELLOW, styles=_BOLD),
        skipped=StatusMarker(label="∅", color=TerminalColor.LIGHT_BLACK, styles=_DIM),
    )
    MARKERS_PRESET_OK_KO: ClassVar[LeaderLineMarkers] = LeaderLineMarkers(
        pending=StatusMarker(label="[…]", color=TerminalColor.LIGHT_BLACK, styles=_DIM),
        success=StatusMarker(label="[OK]", color=TerminalColor.GREEN, styles=_BOLD),
        failure=StatusMarker(label="[KO]", color=TerminalColor.RED, styles=_BOLD),
        warning=StatusMarker(label="[!]", color=TerminalColor.YELLOW, styles=_BOLD),
        skipped=StatusMarker(label="[-]", color=TerminalColor.LIGHT_BLACK, styles=_DIM),
    )
    MARKERS_PRESET_PASS_FAIL: ClassVar[LeaderLineMarkers] = LeaderLineMarkers(
        pending=StatusMarker(label="…", color=TerminalColor.LIGHT_BLACK, styles=_DIM),
        success=StatusMarker(label="PASS", color=TerminalColor.GREEN, styles=_BOLD),
        failure=StatusMarker(label="FAIL", color=TerminalColor.RED, styles=_BOLD),
        warning=StatusMarker(label="WARN", color=TerminalColor.YELLOW, styles=_BOLD),
        skipped=StatusMarker(label="SKIP", color=TerminalColor.LIGHT_BLACK, styles=_DIM),
    )

    # --- Instance fields ----------------------------------------------------
    dot_char: str = public_field(
        default=DEFAULT_DOT_CHAR,
        description="Character used for the leader (the dotted bridge).",
    )
    dot_color: TerminalColor | None = public_field(
        default=TerminalColor.LIGHT_BLACK,
        description="Color of the leader dots (subtle grey by default).",
    )
    markers: LeaderLineMarkers = public_field(
        description="Bundle of state→marker mappings driving the right-hand cell."
    )
    message: str = public_field(
        description="Left-hand text — what the line describes."
    )
    state: str = public_field(
        default="pending",
        description="Current lifecycle state — one of pending/success/failure/warning/skipped.",
    )
    status: str | None = public_field(
        default=None,
        description="Optional free-form text rendered after the marker (e.g. error reason).",
    )
    width: int | None = public_field(
        default=None,
        description="Fixed total width; falls back to the context width when None.",
    )
    _handle: LeaderLineHandle | None = None
    _redraw_in_place: bool = False

    @classmethod
    def create_leader_line(
        cls,
        message: str,
        state: str = "pending",
        status: str | None = None,
        markers: LeaderLineMarkers | None = None,
        dot_char: str = DEFAULT_DOT_CHAR,
        dot_color: TerminalColor | None = TerminalColor.LIGHT_BLACK,
        width: int | None = None,
        verbosity: VerbosityLevel | None = None,
    ) -> LeaderLinePromptResponse:
        return cls(
            lines=[],
            message=message,
            state=state,
            status=status,
            markers=markers or cls.MARKERS_PRESET_CHECK,
            dot_char=dot_char,
            dot_color=dot_color,
            width=width,
            verbosity=verbosity,
        )

    @classmethod
    def get_example_class(cls) -> type:
        from wexample_prompt.example.response.interactive.leader_line_example import (
            LeaderLineExample,
        )

        return LeaderLineExample

    def get_handle(self) -> LeaderLineHandle:
        from wexample_prompt.common.leader.leader_line_handle import LeaderLineHandle

        assert isinstance(self._handle, LeaderLineHandle)
        return self._handle

    def init_handle(self, context: PromptContext | None = None) -> PromptContext:
        from wexample_prompt.common.leader.leader_line_handle import LeaderLineHandle
        from wexample_prompt.common.prompt_context import PromptContext

        context = PromptContext.create_if_none(context=context)
        if not self._handle:
            self._handle = LeaderLineHandle(response=self, context=context)
        self._handle.context = context
        return context

    def render(self, context: PromptContext | None = None) -> str | None:
        from wexample_prompt.common.prompt_response_line import PromptResponseLine
        from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
        from wexample_prompt.helper.terminal import terminal_get_visible_width

        context = self.init_handle(context=context)

        marker = self.markers.get(self.state)
        marker_text = marker.label
        status_text = f" {self.status}" if self.status else ""

        message_visible = terminal_get_visible_width(self.message)
        marker_visible = terminal_get_visible_width(marker_text)
        status_visible = terminal_get_visible_width(status_text)

        max_content_width = context.get_available_width(self.width, minimum=0)
        # 2 spaces consumed: one between message and dots, one between dots and marker.
        dot_count = max(
            1,
            max_content_width - message_visible - marker_visible - status_visible - 2,
        )

        segments: list[PromptResponseSegment] = [
            PromptResponseSegment(text=self.message),
            PromptResponseSegment(text=" "),
            PromptResponseSegment(
                text=self.dot_char * dot_count, color=self.dot_color
            ),
            PromptResponseSegment(text=" "),
            PromptResponseSegment(
                text=marker_text, color=marker.color, styles=marker.styles
            ),
        ]
        if status_text:
            segments.append(
                PromptResponseSegment(text=status_text, color=marker.color)
            )

        self.lines = [PromptResponseLine(segments=segments)]
        rendered = super().render(context=context)
        if rendered is not None and self._redraw_in_place:
            # CSI 1A: cursor up one row. CSI 2K: erase entire current line.
            # \r: snap back to col 0 so the new frame overwrites cleanly.
            return f"\x1b[1A\x1b[2K\r{rendered}"
        return rendered
