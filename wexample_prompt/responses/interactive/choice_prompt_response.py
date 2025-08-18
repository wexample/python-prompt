"""Response for displaying and handling choice prompts."""
from typing import Any, List, Optional, Dict, Union, Type, TYPE_CHECKING

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.utils import InquirerPyDefault, InquirerPySessionResult
from pydantic import Field, ConfigDict

from wexample_prompt.common.color_manager import ColorManager
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.enums.text_style import TextStyle
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
    default: Optional[InquirerPyDefault] = Field(
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
    def optional_color(cls, text: str, color: TerminalColor, colorize: bool) -> str:
        return ColorManager.colorize(text, color) if colorize else text

    @classmethod
    def create_choice(
        cls,
        question: str,
        choices: List[Any],
        context: Optional[PromptContext] = None,
        default: Optional[InquirerPyDefault] = None,
        abort: Optional[str] = "> Abort",
        color: Optional[TerminalColor] = None,
        verbosity: VerbosityLevel = VerbosityLevel.DEFAULT
    ) -> "ChoicePromptResponse":
        lines: List[PromptResponseLine] = []

        colorize = False if color is False else True

        lines.append(
            PromptResponseLine(
                segments=[
                    PromptResponseSegment(
                        text=cls.optional_color(
                            question, color if color else TerminalColor.BLUE, colorize
                        ),
                        styles=[TextStyle.BOLD],
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
                            text=cls.optional_color(f"  {i + 1}. → ", TerminalColor.CYAN, colorize)
                        ),
                        PromptResponseSegment(
                            text=cls.optional_color(choice_text, TerminalColor.WHITE, colorize),
                            styles=[TextStyle.DIM],
                        ),
                    ]
                )
            )

        original_context_color_enabled = None
        if context is not None:
            original_context_color_enabled = context.colorized
            context.colorized = colorize

        if context is None:
            context = PromptContext(colorized=colorize)

        response = cls(
            lines=lines,
            choices=choices_all,
            default=default,
            question_text=question,
            verbosity=verbosity,
        )

        if original_context_color_enabled is not None:
            context.colorized = original_context_color_enabled

        return response

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        from wexample_prompt.example.response.interactive.choice_example import ChoiceExample
        return ChoiceExample
