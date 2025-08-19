"""Mixin for managing file picker prompt responses."""
from typing import Optional, TYPE_CHECKING

from wexample_helpers.const.types import Kwargs
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.choice import FilePickerMode

if TYPE_CHECKING:
    from wexample_prompt.responses.interactive.file_picker_prompt_response import FilePickerPromptResponse
    from wexample_prompt.common.io_manager import IoManager


class FilePickerPromptResponseManagerMixin:
    """Mixin class for managing file picker prompt responses."""

    def file_picker(
            self: "IoManager",
            question: str = "Select a file:",
            base_dir: Optional[str] = None,
            abort: Optional[bool | str]  = None,
            mode: FilePickerMode = FilePickerMode.BOTH,
            allow_parent_selection: bool = False,
            reset_on_finish: bool = False,
            context: Optional[PromptContext] = None,
            **kwargs: Kwargs,
    ) -> "FilePickerPromptResponse":
        from wexample_prompt.responses.interactive.file_picker_prompt_response import FilePickerPromptResponse

        response = FilePickerPromptResponse.create_file_picker(
            question=question,
            base_dir=base_dir,
            abort=abort,
            mode=mode,
            allow_parent_selection=allow_parent_selection,
            reset_on_finish=reset_on_finish,
            **kwargs,
        )

        return self.print_response(
            response=response,
            context=FilePickerPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
        )
