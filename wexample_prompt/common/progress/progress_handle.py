from typing import Optional, TYPE_CHECKING, Union

from pydantic import Field

from wexample_helpers.classes.extended_base_model import ExtendedBaseModel
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.output.abstract_output_handler import AbstractOutputHandler
from wexample_prompt.responses.interactive.progress_prompt_response import ProgressPromptResponse

if TYPE_CHECKING:
    from wexample_prompt.enums.terminal_color import TerminalColor
    from wexample_prompt.common.progress.range_progress_handle import RangeProgressHandle


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
            current: Optional[Union[float, int, str]] = None,
            label: Optional[str] = None,
            color: Optional["TerminalColor"] = None,
            auto_render: bool = True,
    ) -> Optional[str]:
        """Update progress fields and optionally re-render."""
        if current is not None:
            # Accept percentage strings like '54%'
            self.response.current = ProgressPromptResponse._normalize_value(self.response.total, current)
        if label is not None:
            self.response.label = label
        if color is not None:
            self.response.color = color

        if auto_render:
            return self.render()
        return None

    def advance(
            self,
            step: Optional[Union[float, int, str]] = None,
            **kwargs
    ) -> Optional[str]:
        step = ProgressPromptResponse._normalize_value(self.response.total, step)

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

    # --- Sub-range API ---
    def create_range_handle(
            self,
            *,
            to: Optional[int] = None,
            from_: Optional[int] = None,
            total: Optional[int] = None,
    ) -> "RangeProgressHandle":
        from wexample_prompt.common.progress.range_progress_handle import RangeProgressHandle

        """Create a handle that controls only a sub-range of the parent handle.

        Rules:
        - If from_ is None, it defaults to the current parent progress.
        - Specify either `to` or `total` (or both). If both, they must be consistent.
        - Effective child total = total if provided else (to - from_).
        - The sub-range maps child's [0..child_total] onto parent's [from_..end].
        """
        start = from_ if from_ is not None else self.response.current
        if total is None and to is None:
            raise ValueError("create_range_handle requires at least 'to' or 'total'")
        if total is None:
            total = int(to - start)  # type: ignore[arg-type]
        if total < 0:
            raise ValueError("Sub-range total must be >= 0")
        end = start + total
        # Clamp to parent bounds
        start = max(0, min(self.response.total, start))
        end = max(0, min(self.response.total, end))
        if end < start:
            start, end = end, start
        return RangeProgressHandle(parent=self, start=start, end=end, total=(end - start))
