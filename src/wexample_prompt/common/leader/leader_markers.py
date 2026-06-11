"""Status markers for LeaderLinePromptResponse.

A `LeaderLineMarkers` bundle is what tells the leader-line widget which
text/color/style to display for each life-cycle state (pending → success
or failure). The widget ships built-in presets (CHECK, OK_KO, PASS_FAIL)
modeled after the confirm widget's `MAPPING_PRESET_*` pattern, and any
caller can pass a fully custom bundle when their layout needs it.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_prompt.enums.terminal_color import TerminalColor
    from wexample_prompt.enums.text_style import TextStyle


@base_class
class StatusMarker(BaseClass):
    """One visible cell of a leader-line state (pending/success/failure/…)."""

    color: TerminalColor | None = public_field(
        default=None, description="Optional foreground color for the marker."
    )
    label: str = public_field(description="The marker text rendered after the dots.")
    styles: list[TextStyle] = public_field(
        factory=list,
        description="Optional ANSI text styles applied to the marker (bold, dim, …).",
    )


@base_class
class LeaderLineMarkers(BaseClass):
    """Bundle of state→marker mappings consumed by `LeaderLinePromptResponse`.

    ``pending`` / ``success`` / ``failure`` are mandatory because every
    leader line transitions through them. ``warning`` and ``skipped`` are
    optional escape hatches for richer flows (e.g. test runners that want
    to surface a "this passed but with a non-fatal note" outcome).
    """

    failure: StatusMarker = public_field(description="Marker for the failure state.")
    pending: StatusMarker = public_field(
        description="Marker shown before success/failure is decided."
    )
    skipped: StatusMarker | None = public_field(
        default=None,
        description="Optional marker when the operation was deliberately skipped.",
    )
    success: StatusMarker = public_field(description="Marker for the success state.")
    warning: StatusMarker | None = public_field(
        default=None,
        description="Optional marker for a non-fatal warning outcome.",
    )

    def get(self, state: str) -> StatusMarker:
        marker = getattr(self, state, None)
        if marker is None:
            raise ValueError(
                f"State '{state}' has no marker in this bundle "
                f"(available: pending/success/failure"
                f"{'/warning' if self.warning else ''}"
                f"{'/skipped' if self.skipped else ''})"
            )
        return marker
