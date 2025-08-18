"""Response for displaying and handling dictionary-based choice prompts."""
from typing import Any, Dict, Optional, List, Union, Type, TYPE_CHECKING

from InquirerPy.base.control import Choice
from pydantic import Field, ConfigDict

from wexample_prompt.responses.interactive.choice_prompt_response import ChoicePromptResponse
from wexample_prompt.enums.verbosity_level import VerbosityLevel

if TYPE_CHECKING:
    from wexample_prompt.example.abstract_response_example import AbstractResponseExample


class ChoiceDictPromptResponse(ChoicePromptResponse):
    """Display choices from a dictionary and return the selected key."""

    original_choices: Dict[str, str] = Field(
        default_factory=dict,
        description="Original mapping of keys to display labels",
    )

    @classmethod
    def create_choice_dict(
        cls,
        question: str,
        choices: Dict[str, str],
        default: Optional[str] = None,
        abort: Optional[str] = "> Abort",
        verbosity: VerbosityLevel = VerbosityLevel.DEFAULT
    ) -> "ChoiceDictPromptResponse":
        """Create a dictionary-based choice prompt response."""
        choice_list: List[Union[str, Choice]] = []
        for key, value in choices.items():
            choice_list.append(Choice(value=key, name=value))

        response = super().create_choice(
            question=question,
            choices=choice_list,
            default=default,
            abort=abort,
            verbosity=verbosity,
        )

        assert isinstance(response, ChoicePromptResponse)
        # Rebuild into subclass instance preserving fields
        new = cls(
            lines=response.lines,
            choices=response.choices,
            default=response.default,
            inquirer_kwargs=response.inquirer_kwargs,
            question_text=response.question_text,
            original_choices=choices,
        )
        return new

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        from wexample_prompt.example.response.interactive.choice_dict_example import ChoiceDictExample
        return ChoiceDictExample
