"""Mixin for managing file picker prompt responses."""
from typing import Optional, Any

from wexample_prompt.responses.interactive.file_picker_prompt_response import FilePickerPromptResponse


class FilePickerPromptResponseManagerMixin:
    """Mixin class for managing file picker prompt responses."""

    def file_picker(
        self,
        base_dir: Optional[str] = None,
        question: str = "Select a file:",
        **kwargs: Any
    ) -> FilePickerPromptResponse:
        """Create a file picker prompt response.

        Args:
            base_dir: Starting directory (defaults to current working directory)
            question: The question to display
            **kwargs: Additional arguments passed to create_file_picker

        Returns:
            FilePickerPromptResponse: A new file picker prompt response
        """
        response = FilePickerPromptResponse.create_file_picker(
            base_dir=base_dir,
            question=question,
            context=self.create_context(),
            **kwargs
        )
        self.print_response(response)
        return response
