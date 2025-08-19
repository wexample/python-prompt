"""Response for displaying and handling directory picker prompts."""
import os
from typing import Dict, Optional, Type, List, Union

from InquirerPy.base.control import Choice
from pydantic import Field

from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.responses.interactive.choice_prompt_response import ChoicePromptResponse


class DirPickerPromptResponse(ChoicePromptResponse):
    """Response for displaying a directory picker interface."""

    base_dir: str = Field(
        description="Base directory to browse from; defaults to current working directory if not provided",
    )

    @classmethod
    def get_example_class(cls) -> Type:
        from wexample_prompt.example.response.interactive.dir_picker_example import DirPickerExample
        return DirPickerExample

    @classmethod
    def create_dir_picker(
            cls,
            base_dir: Optional[str] = None,
            question: str = "Select a directory:",
            abort: Optional[bool | str]  = None,
            verbosity: VerbosityLevel = VerbosityLevel.DEFAULT
    ) -> "DirPickerPromptResponse":
        base = base_dir or os.getcwd()

        # Build dict of choices: include parent and subdirectories
        choices_dirs: Dict[str, str] = {"..": ".."}
        try:
            for element in os.listdir(base):
                full_path = os.path.join(base, element)
                if os.path.isdir(full_path):
                    choices_dirs[element] = f" {element}"
        except Exception:
            # If listing fails, still allow selecting current dir or parent
            pass

        # Sort by label
        from wexample_helpers.helpers.dict import dict_sort_values
        choices_dirs = dict_sort_values(choices_dirs)

        # Add option to select current directory
        choices_dirs[base] = "> Select this directory"

        # Convert to InquirerPy choices
        choice_list: List[Union[str, Choice]] = [Choice(value=k, name=v) for k, v in choices_dirs.items()]

        # Important: create the base ChoicePromptResponse first to avoid
        # instantiating this subclass (which requires base_dir) prematurely.
        parent_response = ChoicePromptResponse.create_choice(
            question=question,
            choices=choice_list,
            default=None,
            abort=abort,
            verbosity=verbosity,
        )

        # Build final subclass instance preserving fields from parent_response
        new = cls(
            lines=parent_response.lines,
            choices=parent_response.choices,
            default=parent_response.default,
            inquirer_kwargs=parent_response.inquirer_kwargs,
            question=parent_response.question_text,
            base_dir=base,
            verbosity=verbosity,
        )
        return new

    def execute(self) -> Optional[str]:
        selected = super().execute()
        if not selected:
            return None

        # If current directory selected, return it
        if selected == self.base_dir:
            return selected

        # Otherwise compute next path and recurse if it's a directory
        full_path = os.path.join(self.base_dir, selected)
        if os.path.isdir(full_path):
            next_response = self.__class__.create_dir_picker(
                base_dir=full_path,
                question=self.question_text or "Select a directory:",
            )
            return next_response.execute()

        return None
