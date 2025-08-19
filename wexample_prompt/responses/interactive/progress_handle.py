from typing import Optional, TYPE_CHECKING

from pydantic import Field

from wexample_helpers.classes.extended_base_model import ExtendedBaseModel
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.output.abstract_output_handler import AbstractOutputHandler
from wexample_prompt.responses.interactive.progress_prompt_response import ProgressPromptResponse

if TYPE_CHECKING:
    from wexample_prompt.enums.terminal_color import TerminalColor


class ProgressHandle(ExtendedBaseModel):
    """A small stateful handle to drive a progress response over time."""

    response: "ProgressPromptResponse" = Field(
        description="The parent response"
    )
    context: "PromptContext" = Field(
        description="The original rendering context"
    )
    output: Optional["AbstractOutputHandler"] = Field(
        default=None,
        description="The output handler if exists, when called from manager"
    )

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
    ) -> Optional[str]:
        """Update progress fields and optionally re-render."""
        if current is not None:
            self.response.current = max(0, current)
        if label is not None:
            self.response.label = label
        if color is not None:
            self.response.color = color

        if auto_render:
            return self.render()
        return None

    def advance(
            self,
            step: int = 1,
            **kwargs
    ) -> Optional[str]:
        """Increment progress by a number of steps and optionally render."""
        return self.update(
            current=max(0, self.response.current + step),
            **kwargs
        )

    def finish(self, **kwargs) -> Optional[str]:
        return self.update(
            current=self.response.total,
            **kwargs
        )
