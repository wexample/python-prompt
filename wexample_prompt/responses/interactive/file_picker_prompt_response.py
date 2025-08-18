"""Response for displaying and handling file picker prompts."""
import os
from typing import Any, Dict, Optional, Type, List, Union

from InquirerPy.base.control import Choice
from pydantic import Field

from wexample_prompt.responses.interactive.choice_prompt_response import ChoicePromptResponse
from wexample_prompt.responses.interactive.choice_dict_prompt_response import ChoiceDictPromptResponse


class FilePickerPromptResponse(ChoiceDictPromptResponse):
    """Response for displaying a file picker interface."""

    base_dir: str = Field(description="Base directory to browse from; defaults to current working directory if not provided")

    @classmethod
    def get_example_class(cls) -> Type:
        from wexample_prompt.example.response.interactive.file_picker_example import FilePickerExample
        return FilePickerExample

    @classmethod
    def create_file_picker(
        cls,
        base_dir: Optional[str] = None,
        question: str = "Select a file:",
        abort: Optional[str] = "> Abort",
        **kwargs: Any,
    ) -> "FilePickerPromptResponse":
        base = base_dir or os.getcwd()

        # Separate directories and files for better organization
        choices_dirs: Dict[str, str] = {"..": ".."}
        choices_files: Dict[str, str] = {}
        try:
            for element in os.listdir(base):
                full_path = os.path.join(base, element)
                if os.path.isdir(full_path):
                    choices_dirs[element] = f" {element}"
                else:
                    choices_files[element] = element
        except Exception:
            pass

        # Sort
        try:
            from wexample_helpers.helpers.dict import dict_merge, dict_sort_values
            choices_dirs = dict_sort_values(choices_dirs)
            choices_files = dict_sort_values(choices_files)
            merged = dict_merge(choices_dirs, choices_files)
        except Exception:
            choices_dirs = dict(sorted(choices_dirs.items(), key=lambda kv: kv[1]))
            choices_files = dict(sorted(choices_files.items(), key=lambda kv: kv[1]))
            merged = {**choices_dirs, **choices_files}

        # Convert to InquirerPy choices
        choice_list: List[Union[str, Choice]] = [Choice(value=k, name=v) for k, v in merged.items()]

        parent_response = ChoicePromptResponse.create_choice(
            question=question,
            choices=choice_list,
            default=None,
            abort=abort,
        )

        new = cls(
            lines=parent_response.lines,
            choices=parent_response.choices,
            default=parent_response.default,
            inquirer_kwargs=parent_response.inquirer_kwargs,
            question_text=parent_response.question_text,
            original_choices={k: v for k, v in merged.items()},
            base_dir=base,
        )
        return new

    def execute(self) -> Optional[str]:
        selected = super().execute()
        if not selected:
            return None

        full_path = os.path.join(self.base_dir, selected)

        if os.path.isdir(full_path):
            next_response = self.__class__.create_file_picker(
                base_dir=full_path,
                question=self.question_text or "Select a file:",
            )
            return next_response.execute()

        return full_path
