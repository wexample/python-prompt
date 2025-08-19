"""Response for displaying and handling file picker prompts."""
import os
from typing import Dict, Optional, Type, Any

from pydantic import Field

from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.enums.choice import FilePickerMode
from wexample_prompt.responses.interactive.choice_prompt_response import ChoicePromptResponse


class FilePickerPromptResponse(ChoicePromptResponse):
    """Response for displaying a file picker interface."""

    base_dir: str = Field(
        description="Base directory to browse from; defaults to current working directory if not provided")
    mode: FilePickerMode = Field(
        default=FilePickerMode.BOTH,
        description="Filter entries: files, dirs, or both (default). Affects visibility, not just selection."
    )
    abort_option: Optional[bool | str] = Field(
        default=None,
        description="Abort configuration forwarded to inner ChoicePromptResponse (bool or custom label)."
    )
    allow_parent_selection: bool = Field(
        default=False,
        description="If True, include '..' as a selectable entry at the top; otherwise hide it."
    )

    @classmethod
    def get_example_class(cls) -> Type:
        from wexample_prompt.example.response.interactive.file_picker_example import FilePickerExample
        return FilePickerExample

    @classmethod
    def create_file_picker(
            cls,
            base_dir: Optional[str] = None,
            question: str = "Select a file:",
            abort: Optional[bool | str] = None,
            mode: FilePickerMode = FilePickerMode.BOTH,
            allow_parent_selection: bool = False,
            reset_on_finish: bool = False,
            predefined_answer: Any = None,
            verbosity: VerbosityLevel = VerbosityLevel.DEFAULT
    ) -> "FilePickerPromptResponse":
        base = base_dir or os.getcwd()

        # Build mapping with ".." first, then folders (with icon), then files
        dirs: Dict[str, str] = {}
        files: Dict[str, str] = {}
        try:
            for element in os.listdir(base):
                full_path = os.path.join(base, element)
                if os.path.isdir(full_path):
                    if mode in (FilePickerMode.BOTH, FilePickerMode.DIRS):
                        dirs[element] = f"📁 {element}"
                else:
                    if mode in (FilePickerMode.BOTH, FilePickerMode.FILES):
                        files[element] = element
        except Exception:
            pass

        merged: Dict[str, str] = {}
        if allow_parent_selection:
            merged[".."] = ".."
        for name in sorted(dirs.keys(), key=str.casefold):
            merged[name] = dirs[name]
        for name in sorted(files.keys(), key=str.casefold):
            merged[name] = files[name]

        # Build parent Choice response using mapping (key=value, value=title)
        parent_response = ChoicePromptResponse.create_choice(
            question=question,
            choices=merged,
            default=None,
            abort=abort,
            verbosity=verbosity,
            reset_on_finish=reset_on_finish,
            predefined_answer=predefined_answer,
        )

        return cls(
            # Do not copy lines; ChoicePromptResponse.ask rebuilds lines each frame
            choices=parent_response.choices,
            default=parent_response.default,
            inquirer_kwargs=parent_response.inquirer_kwargs,
            question=parent_response.question,
            question_line=parent_response.question_line,
            base_dir=base,
            mode=mode,
            abort_option=abort,
            verbosity=verbosity,
            reset_on_finish=reset_on_finish,
            predefined_answer=predefined_answer,
        )

