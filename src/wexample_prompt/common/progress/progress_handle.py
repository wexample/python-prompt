from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.output.abstract_output_handler import AbstractOutputHandler

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.enums.terminal_color import TerminalColor
    from wexample_prompt.output.abstract_output_handler import AbstractOutputHandler
    from wexample_prompt.responses.interactive.progress_prompt_response import (
        ProgressPromptResponse,
    )


@base_class
class ProgressHandle(BaseClass):
    """Stateful progress handle.

    Can directly control a root response or map a child range onto a parent handle.
    Supports arbitrary nesting (child of child, etc.).
    """

    context: PromptContext = public_field(
        description="The rendering context used by the response."
    )
    output: AbstractOutputHandler | None = public_field(
        default=None, description="Optional output handler when used via IoManager."
    )
    parent: ProgressHandle | None = public_field(
        default=None,
        description="Parent handle if this handle controls a sub-range of another handle.",
    )
    range_end: int | None = public_field(
        default=None,
        description="Exclusive end position on the parent response for this sub-range (absolute units).",
    )
    range_start: int | None = public_field(
        default=None,
        description="Inclusive start position on the parent response for this sub-range (absolute units).",
    )
    response: ProgressPromptResponse = public_field(
        description="The associated progress response (root response)."
    )

    # --- Public properties ---
    @property
    def total(self) -> int:
        """Return the effective total for this handle.

        - For a child handle, it's the size of the mapped range (range_end - range_start).
        - For a root handle, it's the underlying response total.
        """
        return self._effective_total()

    @total.setter
    def total(self, value: int) -> None:
        """Set the total dynamically after creation.

        - For a child handle, adjusts range_end = range_start + value (clamped to parent bounds).
        - For a root handle, sets response.total and clamps response.current.
        """
        if value is None:
            return
        new_total = max(0, int(value))
        if self._is_child():
            # Adjust child absolute end within parent bounds
            start = int(self.range_start)  # type: ignore[arg-type]
            parent_total = (
                self.parent.response.total if self.parent else self.response.total
            )
            end = max(0, min(parent_total, start + new_total))
            # Ensure monotonicity (end >= start)
            if end < start:
                end = start
            self.range_end = end
            # Clamp parent's absolute current to the new range
            if self.response.current < start:
                self.response.current = start
            if self.response.current > end:
                self.response.current = end
        else:
            # Root: enforce strictly positive total to keep semantics with creation
            if new_total <= 0:
                raise ValueError("Total must be greater than 0")
            self.response.total = new_total
            # Clamp current to new total
            if self.response.current > new_total:
                self.response.current = new_total

    def advance(self, step: float | int | str | None = None, **kwargs) -> str | None:
        """Increment progress by a number of steps and optionally render."""
        from wexample_prompt.responses.interactive.progress_prompt_response import (
            ProgressPromptResponse,
        )

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

    # --- Sub-range API ---
    def create_range_handle(
        self,
        *,
        to: int | None = None,
        from_: int | None = None,
        total: int | None = None,
        to_step: int | None = None,
    ) -> ProgressHandle:
        """Create a child handle that controls only a sub-range of this handle.

        Rules:
        - If from_ is None, it defaults to the current parent progress.
        - You can specify one of:
          - `total` (explicit size of the child range), or
          - `to` (absolute end bound on the parent; child size = to - from_), or
          - `to_step` (relative size from the start, i.e. child size = to_step).
          If multiple are provided, `total` takes precedence, then `to`, then `to_step`.
        - The sub-range maps child's [0..child_total] onto parent's [from_..end].
        """
        start = from_ if from_ is not None else self.response.current
        if total is None and to is None and to_step is None:
            raise ValueError(
                "create_range_handle requires one of 'total', 'to', or 'to_step'"
            )
        if total is None:
            if to is not None:
                total = int(to - start)  # type: ignore[arg-type]
            else:
                total = int(to_step)  # type: ignore[arg-type]
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

    def finish(self, **kwargs) -> str | None:
        if self._is_child():
            # Set absolute end on shared response
            self.response.current = int(self.range_end)  # type: ignore[arg-type]
            return self.update(current=None, **kwargs)
        return self.update(current=self.response.total, **kwargs)

    def render(self) -> str:
        """Render once using the stored context and optional output handler."""
        if self.output is not None:
            return self.output.print(self.response, context=self.context)
        return self.response.render(context=self.context)

    def update(
        self,
        current: float | int | str | None = None,
        label: str | None = None,
        color: TerminalColor | None = None,
        total: int | None = None,
        to: int | None = None,
        auto_render: bool = True,
    ) -> str | None:
        """Update progress fields and optionally re-render.

        If this handle is a child, `current` is interpreted relative to the child range
        and mapped to the parent's absolute scale.
        """
        from wexample_prompt.responses.interactive.progress_prompt_response import (
            ProgressPromptResponse,
        )

        if self._is_child():
            # Dynamic range adjustments first so that current mapping uses latest bounds
            if total is not None:
                # Set child total relative to start
                self.total = int(total)
            if to is not None:
                # Set absolute end bound within parent
                parent_total = (
                    self.parent.response.total if self.parent else self.response.total
                )
                new_end = max(0, min(parent_total, int(to)))
                start = int(self.range_start)  # type: ignore[arg-type]
                if new_end < start:
                    new_end = start
                self.range_end = new_end
                # Clamp absolute current to new bounds
                if self.response.current < start:
                    self.response.current = start
                if self.response.current > new_end:
                    self.response.current = new_end

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
            # Root adjustments
            if total is not None:
                self.total = int(total)
            if to is not None:
                # Alias for total at root level
                self.total = int(to)
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

    def _child_current(self) -> int:
        # Derive child-relative current from parent's absolute current
        if not self._is_child():
            return self.response.current
        cur = max(self.range_start, min(self.range_end, self.response.current))  # type: ignore[arg-type]
        return max(0, min(self._effective_total(), cur - int(self.range_start)))  # type: ignore[arg-type]

    def _effective_total(self) -> int:
        if self._is_child():
            return max(0, int(self.range_end - self.range_start))  # type: ignore[arg-type]
        return self.response.total

    # --- Internal helpers ---
    def _is_child(self) -> bool:
        return (
            self.parent is not None
            and self.range_start is not None
            and self.range_end is not None
        )
