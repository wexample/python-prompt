from typing import TYPE_CHECKING, Optional, Union

from pydantic import Field
from wexample_helpers.classes.extended_base_model import ExtendedBaseModel
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.output.abstract_output_handler import AbstractOutputHandler
from wexample_prompt.responses.interactive.progress_prompt_response import (
    ProgressPromptResponse,
)

if TYPE_CHECKING:
    from wexample_prompt.enums.terminal_color import TerminalColor


class ProgressHandle(ExtendedBaseModel):
    """Stateful progress handle.

    Can directly control a root response or map a child range onto a parent handle.
    Supports arbitrary nesting (child of child, etc.).
    """

    response: "ProgressPromptResponse" = Field(
        description="The associated progress response (root response)."
    )
    context: "PromptContext" = Field(
        description="The rendering context used by the response."
    )
    output: Optional["AbstractOutputHandler"] = Field(
        default=None, description="Optional output handler when used via IoManager."
    )
    parent: Optional["ProgressHandle"] = Field(
        default=None,
        description="Parent handle if this handle controls a sub-range of another handle.",
    )
    range_start: Optional[int] = Field(
        default=None,
        description="Inclusive start position on the parent response for this sub-range (absolute units).",
    )
    range_end: Optional[int] = Field(
        default=None,
        description="Exclusive end position on the parent response for this sub-range (absolute units).",
    )

    # --- Internal helpers ---
    def _is_child(self) -> bool:
        return (
            self.parent is not None
            and self.range_start is not None
            and self.range_end is not None
        )

    def _effective_total(self) -> int:
        if self._is_child():
            return max(0, int(self.range_end - self.range_start))  # type: ignore[arg-type]
        return self.response.total

    def _child_current(self) -> int:
        # Derive child-relative current from parent's absolute current
        if not self._is_child():
            return self.response.current
        cur = max(self.range_start, min(self.range_end, self.response.current))  # type: ignore[arg-type]
        return max(0, min(self._effective_total(), cur - int(self.range_start)))  # type: ignore[arg-type]

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
        """Update progress fields and optionally re-render.

        If this handle is a child, `current` is interpreted relative to the child range
        and mapped to the parent's absolute scale.
        """
        if self._is_child():
            if current is not None:
                # Normalize against child total; supports percentage strings.
                norm = ProgressPromptResponse._normalize_value(
                    self._effective_total(), current
                )
                mapped = int(self.range_start) + max(0, min(self._effective_total(), norm))  # type: ignore[arg-type]
                # Directly set absolute current on the shared response
                self.response.current = mapped
            if label is not None:
                self.response.label = label
            if color is not None:
                self.response.color = color
            if auto_render:
                return self.render()
            return None
        else:
            if current is not None:
                self.response.current = ProgressPromptResponse._normalize_value(
                    self.response.total, current
                )
            if label is not None:
                self.response.label = label
            if color is not None:
                self.response.color = color

            if auto_render:
                return self.render()
            return None

    def advance(
        self, step: Optional[Union[float, int, str]] = None, **kwargs
    ) -> Optional[str]:
        """Increment progress by a number of steps and optionally render."""
        if self._is_child():
            step_norm = ProgressPromptResponse._normalize_value(
                self._effective_total(), step
            )
            cur_child = self._child_current()
            return self.update(current=cur_child + step_norm, **kwargs)
        else:
            step_val = ProgressPromptResponse._normalize_value(
                self.response.total, step
            )
            return self.update(
                current=max(0, self.response.current + step_val), **kwargs
            )

    def finish(self, **kwargs) -> Optional[str]:
        if self._is_child():
            # Set absolute end on shared response
            self.response.current = int(self.range_end)  # type: ignore[arg-type]
            return self.update(current=None, **kwargs)
        return self.update(current=self.response.total, **kwargs)

    # --- Sub-range API ---
    def create_range_handle(
        self,
        *,
        to: Optional[int] = None,
        from_: Optional[int] = None,
        total: Optional[int] = None,
    ) -> "ProgressHandle":
        """Create a child handle that controls only a sub-range of this handle.

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
        # Create child handle sharing the same response/context/output
        return ProgressHandle(
            response=self.response,
            context=self.context,
            output=self.output,
            parent=self,
            range_start=start,
            range_end=end,
        )
