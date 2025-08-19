"""Response for displaying and handling choice prompts."""
from typing import Any, List, Optional, Dict, Type, TYPE_CHECKING

from pydantic import Field

from wexample_prompt.common.choice.choice import Choice
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.enums.choice import ChoiceValue
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.enums.text_style import TextStyle
from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.responses.interactive.abstract_interactive_prompt_response import (
    AbstractInteractivePromptResponse,
)

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.example.abstract_response_example import AbstractResponseExample


class ChoicePromptResponse(AbstractInteractivePromptResponse):
    """Display a list of choices and get a user selection."""

    choices: List[Choice] = Field(
        default_factory=list,
        description="List of choices",
    )
    default: Optional[Any] = Field(
        default=None,
        description="Default selected value for the prompt"
    )
    inquirer_kwargs: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional kwargs forwarded to inquirer.select"
    )
    question: str = Field(
        default=None,
        description="Question text shown to the user"
    )
    question_line: Optional["PromptResponseLine"] = Field(
        default=None,
        description="The line that displays teh question"
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

        question_line = PromptResponseLine(
            segments=[
                PromptResponseSegment(
                    text=question,
                    color=color or TerminalColor.BLUE,
                    styles=[TextStyle.BOLD],
                )
            ]
        )

        choices_list: List[Choice] = []

        for i, choice in enumerate(choices):
            choices_list.append(Choice(
                value=i,
                title=choice,
                line=PromptResponseLine(segments=[])
            ))

        if abort:
            choices_list.append(
                Choice(
                    value=ChoiceValue.ABORT,
                    title="> Abort",
                    line=PromptResponseLine(segments=[])
                )
            )

        return cls(
            question_line=question_line,
            choices=choices_list,
            default=default,
            question=question,
            verbosity=verbosity,
        )

    def ask(self, context: Optional["PromptContext"] = None) -> Optional[str]:
        import readchar
        idx = 0

        while True:
            print("\033c", end="")
            self.lines = [
                self.question_line
            ]

            for i, choice in enumerate(self.choices):
                line = choice.line

                if i == idx:
                    line.segments = [
                        PromptResponseSegment(text=f"  {i + 1}. → ", color=TerminalColor.BLUE, styles=[TextStyle.BOLD]),
                        PromptResponseSegment(text=str(choice.title), color=TerminalColor.LIGHT_BLUE),
                    ]
                else:
                    line.segments = [
                        PromptResponseSegment(text=f"  {i + 1}. → ", color=TerminalColor.BLUE),
                        PromptResponseSegment(text=str(choice.title), color=TerminalColor.WHITE),
                    ]

                self.lines.append(line)

            print(self.render(context=context))

            key = readchar.readkey()
            if key == readchar.key.UP:
                idx = (idx - 1) % len(self.choices)
            elif key == readchar.key.DOWN:
                idx = (idx + 1) % len(self.choices)
            elif key in (readchar.key.ENTER, "\r", "\n"):
                return str(self.choices[idx].value) if self.choices[idx].value is not None else None

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        from wexample_prompt.example.response.interactive.choice_example import ChoiceExample
        return ChoiceExample
