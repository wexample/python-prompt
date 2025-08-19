"""Mixin for managing progress prompt responses."""
from typing import Any, Optional, TYPE_CHECKING

from wexample_helpers.const.types import Kwargs
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.responses.interactive.progress_prompt_response import ProgressPromptResponse

if TYPE_CHECKING:
    from wexample_prompt.common.io_manager import IoManager


class ProgressPromptResponseManagerMixin:
    """Mixin class for managing progress prompt responses."""

    def progress(
            self: "IoManager",
            total: int,
            current: int,
            width: Optional[int] = None,
            label: Optional[str] = None,
            context: Optional["PromptContext"] = None,
            **kwargs: Kwargs,
    ) -> Any:
        response = ProgressPromptResponse.create_progress(
            total=total,
            current=current,
            width=width,
            label=label,
        )

        return self.print_response(
            response=response,
            context=ProgressPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            )
        )
