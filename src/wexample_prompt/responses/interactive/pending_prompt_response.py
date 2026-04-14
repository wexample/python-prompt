from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, ClassVar

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.interactive.abstract_interactive_prompt_response import (
    AbstractInteractivePromptResponse,
)

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.example.abstract_response_example import (
        AbstractResponseExample,
    )


@base_class
class PendingPromptResponse(AbstractInteractivePromptResponse):
    """Live-polling response that shows a spinner and output lines until a condition is met.

    The callback is called repeatedly and must return (is_ready, output_lines).
    Output lines are displayed in a muted color below the spinner header, similar
    to how docker build shows RUN output in grey during image builds.
    """

    SPINNER_KEY: ClassVar[str] = "pending"
    callback: Callable[[], tuple[bool, list[str]]] = public_field(
        description="Called on each poll; returns (is_ready, output_lines). "
        "The loop exits when is_ready is True.",
    )
    interval: float = public_field(
        default=2.0,
        description="Seconds to sleep between polls.",
    )
    label: str = public_field(
        default="Waiting...",
        description="Label displayed next to the spinner on the header line.",
    )
    max_lines: int = public_field(
        default=5,
        description="Maximum number of output lines to display below the header.",
    )
    output_color: TerminalColor | None = public_field(
        default=TerminalColor.LIGHT_BLACK,
        description="Color applied to output lines. None for terminal default.",
    )

    @classmethod
    def create_pending(
        cls,
        callback: Callable[[], tuple[bool, list[str]]],
        *,
        label: str = "Waiting...",
        interval: float = 2.0,
        max_lines: int = 5,
        output_color: TerminalColor | None = TerminalColor.LIGHT_BLACK,
        reset_on_finish: bool = False,
    ) -> PendingPromptResponse:
        return cls(
            callback=callback,
            label=label,
            interval=interval,
            max_lines=max_lines,
            output_color=output_color,
            reset_on_finish=reset_on_finish,
        )

    @classmethod
    def get_example_class(cls) -> type[AbstractResponseExample]:
        from wexample_prompt.example.response.interactive.pending_example import (
            PendingExample,
        )

        return PendingExample

    def render(self, context: PromptContext | None = None) -> str | None:
        import time

        from wexample_prompt.common.prompt_context import PromptContext
        from wexample_prompt.common.prompt_response_line import PromptResponseLine
        from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
        from wexample_prompt.common.spinner_pool import SpinnerPool

        context = PromptContext.create_if_none(context=context)
        printed_lines = 0

        while True:
            is_ready, output_lines = self.callback()

            spinner_frame = SpinnerPool.next(key=self.SPINNER_KEY)
            self.lines = [
                PromptResponseLine(
                    segments=[
                        PromptResponseSegment(text=f"{spinner_frame} {self.label}")
                    ]
                )
            ]
            for raw_line in output_lines[-self.max_lines :]:
                stripped = raw_line.rstrip()
                if stripped:
                    self.lines.append(
                        PromptResponseLine(
                            segments=[
                                PromptResponseSegment(
                                    text=f"  {stripped}",
                                    color=self.output_color,
                                )
                            ]
                        )
                    )

            self._partial_clear(printed_lines)
            printed_lines = self._print_render(context=context)

            if is_ready:
                if self.reset_on_finish:
                    self._partial_clear(printed_lines)
                return None

            time.sleep(self.interval)
