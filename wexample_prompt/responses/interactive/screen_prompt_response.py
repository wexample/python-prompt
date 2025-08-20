from typing import Any, Callable, Optional, Type

from pydantic import Field

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.responses.interactive.abstract_interactive_prompt_response import (
    AbstractInteractivePromptResponse,
)


class ScreenPromptResponse(AbstractInteractivePromptResponse):
    """A simple screen-like interactive response that repeatedly invokes a user-provided
    callback, allowing the callback to draw text lines, sleep, and request reload/close."""

    callback: Callable[["ScreenPromptResponse"], Any] = Field(
        description="Function called repeatedly with this response instance to draw and control flow.",
    )
    height: int = Field(
        default=30,
        description="Approx height in lines reserved for this response block.",
    )
    reset_on_finish: bool = Field(
        default=False,
        description="If True, clears printed block when finishing (close).",
    )

    _closed: bool = False
    _reload_requested: bool = False

    @classmethod
    def create_screen(
        cls,
        callback: Callable[["ScreenPromptResponse"], Any],
        *,
        height: int = 30,
        reset_on_finish: bool = False,
        verbosity: VerbosityLevel = VerbosityLevel.DEFAULT,
    ) -> "ScreenPromptResponse":
        return cls(
            callback=callback,
            height=height,
            reset_on_finish=reset_on_finish,
            verbosity=verbosity,
        )

    # Drawing helpers for the callback
    def clear(self) -> None:
        self.lines = []

    def print(self, text: str, *, color: Optional[TerminalColor] = None) -> None:
        self.lines.append(
            PromptResponseLine(
                segments=[
                    PromptResponseSegment(
                        text=text,
                        color=color or TerminalColor.RESET,
                        styles=[],
                    )
                ]
            )
        )

    def reload(self) -> None:
        self._reload_requested = True

    def close(self) -> None:
        self._closed = True

    def render(self, context: Optional["PromptContext"] = None) -> Optional[str]:
        # Screen runs a simple controlled loop until closed.
        from time import sleep
        from wexample_prompt.common.prompt_context import PromptContext

        context = PromptContext.create_if_none(context=context)
        # Disable extra formatting to avoid extra lines
        context.formatting = False

        printed_lines = 0
        # First frame: let the callback populate content
        try:
            self._reload_requested = False
            self.callback(self)
        except Exception:
            # If callback errors, close gracefully
            self._closed = True

        while True:
            # Clear previous frame area
            self._partial_clear(printed_lines)

            # Render and print current lines
            printed_lines = self._print_render(context=context)

            if self._closed:
                if self.reset_on_finish and printed_lines > 0:
                    self._partial_clear(printed_lines)
                return None

            # Prepare next frame
            self._reload_requested = False
            try:
                self.callback(self)
            except Exception:
                self._closed = True
                continue

            # If callback didn't request reload and not closed, avoid busy loop
            if not self._reload_requested and not self._closed:
                sleep(0.05)

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        from wexample_prompt.example.response.interactive.choice_example import ChoiceExample  # type: ignore
        # Reuse any example class infra; a dedicated Screen example can be added later.
        return ChoiceExample
