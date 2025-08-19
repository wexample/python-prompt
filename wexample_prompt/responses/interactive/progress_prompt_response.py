"""Progress bar response implementation."""
from typing import List, Callable, Optional, Any, ClassVar, Type

from pydantic import Field

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse

try:
    # Optional import, only needed for step-based execution helpers
    from wexample_prompt.progress.step_progress_context import (
        ProgressStep,
        StepProgressContext,
    )
except Exception:  # pragma: no cover - module may not be present in minimal envs
    ProgressStep = Any  # type: ignore
    StepProgressContext = Any  # type: ignore


class ProgressPromptResponse(AbstractPromptResponse):
    """Response for displaying progress bars."""

    # Style characters
    FILL_CHAR: ClassVar[str] = "▰"
    EMPTY_CHAR: ClassVar[str] = "▱"

    # Instance fields
    total: int = Field(description="Total number of items (must be > 0)")
    current: int = Field(description="Current progress (must be >= 0)")
    width: int = Field(default=50, description="Width of the progress bar in characters")
    label: Optional[str] = Field(default=None, description="Optional label displayed before the bar")
    color: Optional[TerminalColor] = Field(default=None, description="Optional color applied to the bar")

    @classmethod
    def get_example_class(cls) -> Type:
        from wexample_prompt.example.response.interactive.progress_example import ProgressExample
        return ProgressExample

    @classmethod
    def set_style(cls, fill_char: str = "▰", empty_char: str = "▱") -> None:
        """Set the progress bar characters."""
        cls.FILL_CHAR = fill_char
        cls.EMPTY_CHAR = empty_char

    @classmethod
    def create_progress(
            cls,
            total: int,
            current: int,
            width: int = 50,
            label: Optional[str] = None,
            color: Optional[TerminalColor] = None,
            verbosity: VerbosityLevel = VerbosityLevel.DEFAULT
    ) -> "ProgressPromptResponse":
        if total <= 0:
            raise ValueError("Total must be greater than 0")
        if current < 0:
            raise ValueError("Current progress cannot be negative")
        if width < 1:
            raise ValueError("Width must be at least 1")

        return cls(
            lines=[],
            total=total,
            current=current,
            width=width,
            label=label,
            color=color or TerminalColor.BLUE,
            verbosity=verbosity
        )

    def render(self, context: Optional["PromptContext"] = None) -> Optional[str]:
        current = min(self.current, self.total)
        percentage = min(100, int(100 * current / self.total))
        filled = int(self.width * current / self.total)

        context = PromptContext.create_if_none(context=context)
        if context.colorized and self.color:
            color_prefix = str(self.color)
            color_suffix = "\x1b[0m"
        else:
            color_prefix = ""
            color_suffix = ""

        bar = (
                color_prefix + self.FILL_CHAR * filled + self.EMPTY_CHAR * (self.width - filled) + color_suffix
        )

        text = f"{self.label} {bar} {percentage}%" if self.label else f"{bar} {percentage}%"
        self.lines = [PromptResponseLine(segments=[PromptResponseSegment(text=text)])]
        return super().render(context=context)

    # Step helpers below mirror the legacy API. They require ProgressStep/StepProgressContext.
    @classmethod
    def create_steps(
            cls,
            steps: List["ProgressStep"],
            width: int = 50,
            title: Optional[str] = None,
            verbosity: VerbosityLevel = VerbosityLevel.DEFAULT
    ) -> "StepProgressContext":
        total_weight = sum(step.weight for step in steps)
        return StepProgressContext(
            steps=steps,
            total_weight=total_weight,
            width=width,
            title=title,
            verbosity=verbosity,
        )

    @classmethod
    def execute(
            cls,
            callbacks: List[Callable[..., Any]],
            width: int = 50,
            title: Optional[str] = None,
            context: Optional[PromptContext] = None,
    ) -> List[Any]:
        steps: List["ProgressStep"] = []
        for callback in callbacks:
            import inspect

            doc = inspect.getdoc(callback)
            description = doc.split("\n")[0] if doc else callback.__name__
            steps.append(ProgressStep(callback=callback, description=description, weight=1))

        with cls.create_steps(steps, width, title, context) as progress:
            return progress.execute_steps()
