"""Mixin for managing file picker prompt responses."""
from typing import Optional, Any, TYPE_CHECKING

from wexample_helpers.const.types import Kwargs
from wexample_prompt.common.prompt_context import PromptContext

if TYPE_CHECKING:
    from wexample_prompt.responses.interactive.file_picker_prompt_response import FilePickerPromptResponse


class FilePickerPromptResponseManagerMixin:
    """Mixin class for managing file picker prompt responses."""

    def file_picker(
        self,
        question: str = "Select a file:",
        base_dir: Optional[str] = None,
        abort: Optional[str] = "> Abort",
        context: Optional[PromptContext] = None,
        **kwargs: Kwargs,
    ) -> "FilePickerPromptResponse":
        from wexample_prompt.responses.interactive.file_picker_prompt_response import FilePickerPromptResponse

        response = FilePickerPromptResponse.create_file_picker(
            question=question,
            base_dir=base_dir,
            abort=abort,
            **kwargs,
        )

        self.print_response(
            response=response,
            context=FilePickerPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
        )
        return response

