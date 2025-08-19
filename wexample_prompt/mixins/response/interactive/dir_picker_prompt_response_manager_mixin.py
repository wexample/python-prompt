"""Mixin for managing directory picker prompt responses."""
from typing import Optional, TYPE_CHECKING

from wexample_helpers.const.types import Kwargs
from wexample_prompt.common.prompt_context import PromptContext

if TYPE_CHECKING:
    from wexample_prompt.responses.interactive.dir_picker_prompt_response import DirPickerPromptResponse
    from wexample_prompt.common.io_manager import IoManager


class DirPickerPromptResponseManagerMixin:
    """Mixin class for managing directory picker prompt responses."""

    def dir_picker(
            self: "IoManager",
            question: str = "Select a directory:",
            base_dir: Optional[str] = None,
            abort: Optional[bool | str]  = None,
            context: Optional[PromptContext] = None,
            **kwargs: Kwargs,
    ) -> "DirPickerPromptResponse":
        from wexample_prompt.responses.interactive.dir_picker_prompt_response import DirPickerPromptResponse

        response = DirPickerPromptResponse.create_dir_picker(
            question=question,
            base_dir=base_dir,
            abort=abort,
            **kwargs,
        )

        return self.print_response(
            response=response,
            context=DirPickerPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
        )
