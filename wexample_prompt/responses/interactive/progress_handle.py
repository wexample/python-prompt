from typing import Optional, TYPE_CHECKING

from wexample_helpers.classes.extended_base_model import ExtendedBaseModel

if TYPE_CHECKING:
    from wexample_prompt.enums.terminal_color import TerminalColor
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.output.abstract_output_handler import AbstractOutputHandler
    from wexample_prompt.responses.interactive.progress_prompt_response import ProgressPromptResponse


class ProgressHandle(ExtendedBaseModel):
    """A small stateful handle to drive a progress response over time."""

    response: "ProgressPromptResponse"
    context: "PromptContext"
    output: Optional["AbstractOutputHandler"] = None

    def render(self) -> str:
        """Render once using the stored context and optional output handler."""
        if self.output is not None:
            return self.output.print(self.response, context=self.context)
        return self.response.render(context=self.context)

    def update(
            self,
            current: Optional[int] = None,
            label: Optional[str] = None,
            color: Optional["TerminalColor"] = None,
            auto_render: bool = True,
    ) -> "ProgressHandle":
        """Update progress fields and optionally re-render."""
        if current is not None:
            self.response.current = max(0, current)
        if label is not None:
            self.response.label = label
        if color is not None:
            self.response.color = color

        if auto_render:
            self.render()
        return self

    def advance(self, steps: int = 1, auto_render: bool = True) -> "ProgressHandle":
        """Increment progress by a number of steps and optionally render."""
        return self.update(
            current=max(0, self.response.current + steps),
            auto_render=auto_render
        )

    def finish(self, auto_render: bool = True) -> "ProgressHandle":
        """Mark progress as complete (current == total)."""
        self.response.current = self.response.total
        if auto_render:
            self.render()
        return self
