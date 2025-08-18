"""Confirmation dialog interactive response."""
from typing import Any, Dict, List, Optional, Type, Union

from InquirerPy.base.control import Choice
from pydantic import Field

from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.responses.interactive.choice_prompt_response import ChoicePromptResponse


class ConfirmPromptResponse(ChoicePromptResponse):
    """Response for a confirmation dialog with customizable options."""

    original_choices: Dict[str, str] = Field(
        default_factory=dict,
        description="Original mapping of choice values to display names for the confirmation dialog",
    )

    @classmethod
    def get_example_class(cls) -> Type:
        from wexample_prompt.example.response.interactive.confirm_example import ConfirmExample
        return ConfirmExample

    @staticmethod
    def _build_choices_from_dict(choices: Dict[str, str]) -> List[Choice]:
        return [Choice(value=value, name=name) for value, name in choices.items()]

    @classmethod
    def create_confirm(
        cls,
        question: str = "Please confirm:",
        choices: Optional[Dict[str, str]] = None,
        preset: Optional[str] = None,
        default: Optional[str] = None,
        abort: Optional[str] = "> Abort",
        verbosity: VerbosityLevel = VerbosityLevel.DEFAULT
    ) -> "ConfirmPromptResponse":
        """Create a confirmation dialog response.

        Args:
            question: The question text to display.
            choices: Mapping of values -> display names for options. If not provided, uses a preset.
            preset: Optional preset name among {'yes_no', 'ok_cancel', 'yes_no_all', 'continue_cancel'}.
            default: Optional default value matching one of the provided values.
            abort: Optional abort label.
            **kwargs: Additional keyword args forwarded to ChoicePromptResponse.create_choice.
        """
        if choices is None:
            preset = preset or "yes_no"
            if preset == "yes_no":
                choices = {"yes": "Yes", "no": "No"}
            elif preset == "ok_cancel":
                choices = {"ok": "Ok", "cancel": "Cancel"}
            elif preset == "yes_no_all":
                choices = {"yes": "Yes", "no": "No", "yes_all": "Yes to all"}
            elif preset == "continue_cancel":
                choices = {"continue": "Continue", "cancel": "Cancel"}
            else:
                raise ValueError(f"Unknown confirm preset: {preset}")

        # Convert to InquirerPy choices
        choice_list = cls._build_choices_from_dict(choices)

        parent = ChoicePromptResponse.create_choice(
            question=question,
            choices=choice_list,
            default=default,
            abort=abort,
            verbosity=verbosity
        )

        # Build final instance with preserved original choices
        return cls(
            lines=parent.lines,
            choices=parent.choices,
            default=parent.default,
            inquirer_kwargs=parent.inquirer_kwargs,
            question_text=parent.question_text,
            original_choices=choices,
            verbosity=verbosity
        )
