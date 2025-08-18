"""Mixin for managing progress prompt responses."""
from typing import Any, Optional, List, TYPE_CHECKING

from wexample_helpers.const.types import Kwargs
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.responses.interactive.progress_prompt_response import ProgressPromptResponse

if TYPE_CHECKING:
    from wexample_prompt.progress.step_progress_context import ProgressStep
    from wexample_prompt.common.io_manager import IoManager


class ProgressPromptResponseManagerMixin:
    """Mixin class for managing progress prompt responses."""

    def progress(
            self: "IoManager",
            total: int,
            current: int,
            width: int = 50,
            label: Optional[str] = None,
            context: Optional["PromptContext"] = None,
            **kwargs: Kwargs,
    ) -> ProgressPromptResponse:
        response = ProgressPromptResponse.create_progress(
            total=total,
            current=current,
            width=width,
            label=label,
        )

        self.print_response(
            response=response,
            context=ProgressPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            )
        )

        return response

    def progress_steps(
            self,
            steps: List["ProgressStep"],
            width: int = 50,
            title: Optional[str] = None,
            **kwargs: Any,
    ) -> "ProgressPromptResponse":
        return ProgressPromptResponse.create_steps(
            steps=steps,
            width=width,
            title=title,
            **kwargs,
        )

    def progress_execute(
            self,
            callbacks: List[Any],
            width: int = 50,
            title: Optional[str] = None,
            **kwargs: Any,
    ) -> List[Any]:
        return ProgressPromptResponse.execute(
            callbacks=callbacks,
            width=width,
            title=title,
            **kwargs,
        )
