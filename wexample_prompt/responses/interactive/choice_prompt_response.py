"""Response for displaying and handling choice prompts."""
from typing import Any, List, Optional, Dict, Union, Type, TYPE_CHECKING

from InquirerPy.base.control import Choice
from InquirerPy.utils import InquirerPyDefault
from pydantic import Field

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.responses.interactive.abstract_interactive_prompt_response import (
    AbstractInteractivePromptResponse,
)

if TYPE_CHECKING:
    from wexample_prompt.example.abstract_response_example import AbstractResponseExample


class ChoicePromptResponse(AbstractInteractivePromptResponse):
    """Display a list of choices and get a user selection."""

    choices: List[Union[str, Choice]] = Field(
        default_factory=list,
        description="List of choices (plain strings or InquirerPy Choice objects)",
    )
    default: Optional[Any] = Field(
        default=None,
        description="Default selected value for the prompt"
    )
    inquirer_kwargs: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional kwargs forwarded to inquirer.select"
    )
    question_text: str = Field(
        default="",
        description="Question text shown to the user"
    )

    @classmethod
    def create_choice(
            cls,
            question: str,
            choices: List[Any],
            default: Optional[Any] = None,
            abort: Optional[str] = "> Abort",
            color: Optional[TerminalColor] = None,
            verbosity: VerbosityLevel = VerbosityLevel.DEFAULT
    ) -> "ChoicePromptResponse":
        lines: List[PromptResponseLine] = []

        lines.append(
            PromptResponseLine(
                segments=[
                    PromptResponseSegment(
                        text=question,
                        color=color or TerminalColor.BLUE,
                    )
                ]
            )
        )

        choices_all: List[Union[str, Choice]] = list(choices)
        if abort:
            choices_all.append(Choice(value=None, name=abort))

        for i, choice in enumerate(choices_all):
            choice_text = choice.name if isinstance(choice, Choice) else str(choice)
            lines.append(
                PromptResponseLine(
                    segments=[
                        PromptResponseSegment(
                            text=f"  {i + 1}. → ",
                            color=TerminalColor.CYAN
                        ),
                        PromptResponseSegment(
                            text=choice_text,
                            color=TerminalColor.WHITE,
                        ),
                    ]
                )
            )

        return cls(
            lines=lines,
            choices=choices_all,
            default=default,
            question_text=question,
            verbosity=verbosity,
        )

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        from wexample_prompt.example.response.interactive.choice_example import ChoiceExample
        return ChoiceExample
