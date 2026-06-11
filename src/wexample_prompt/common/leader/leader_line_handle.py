"""Stateful handle to mutate a leader-line response after first render.

Mirrors `ProgressHandle`'s ergonomics — the response is printed once,
then the caller flips the state via `success()` / `failure()` and the
handle re-renders the line in place (cursor-up + erase + redraw).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.output.abstract_prompt_output_handler import (
        AbstractPromptOutputHandler,
    )
    from wexample_prompt.responses.interactive.leader_line_prompt_response import (
        LeaderLinePromptResponse,
    )


@base_class
class LeaderLineHandle(BaseClass):
    context: PromptContext = public_field(
        description="Rendering context bound to the leader-line response."
    )
    output: AbstractPromptOutputHandler | None = public_field(
        default=None, description="Optional output handler for in-place re-render."
    )
    response: LeaderLinePromptResponse = public_field(
        description="The leader-line response this handle drives."
    )

    def failure(
        self, status: str | None = None, auto_render: bool = True
    ) -> str | None:
        return self.update(state="failure", status=status, auto_render=auto_render)

    def finish(
        self,
        state: str = "success",
        status: str | None = None,
        auto_render: bool = True,
    ) -> str | None:
        """Convenience: terminate the line in any outcome state."""
        return self.update(state=state, status=status, auto_render=auto_render)

    def render(self) -> str | None:
        # Re-render in place. The response toggles `_redraw_in_place` so
        # `render()` knows to emit `CSI 1A + CSI 2K + \r` before the new
        # frame — same trick as the progress widget.
        self.response._redraw_in_place = True
        try:
            if self.output is not None:
                return self.output.print(self.response, context=self.context)
            return self.response.render(context=self.context)
        finally:
            self.response._redraw_in_place = False

    def skipped(
        self, status: str | None = None, auto_render: bool = True
    ) -> str | None:
        return self.update(state="skipped", status=status, auto_render=auto_render)

    def success(
        self, status: str | None = None, auto_render: bool = True
    ) -> str | None:
        return self.update(state="success", status=status, auto_render=auto_render)

    def update(
        self,
        state: str | None = None,
        status: str | None = None,
        message: str | None = None,
        auto_render: bool = True,
    ) -> str | None:
        if state is not None:
            self.response.state = state
        if status is not None:
            self.response.status = status
        if message is not None:
            self.response.message = message
        if auto_render:
            return self.render()
        return None

    def warning(
        self, status: str | None = None, auto_render: bool = True
    ) -> str | None:
        return self.update(state="warning", status=status, auto_render=auto_render)
