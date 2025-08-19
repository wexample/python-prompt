"""Response for displaying and handling choice prompts."""
from typing import Any, List, Optional, Dict, Union, Type, TYPE_CHECKING

from pydantic import Field

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

    choices: List[Union[str]] = Field(
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
                        styles=[TextStyle.BOLD],
                    )
                ]
            )
        )

        choices_all: List[Union[str]] = list(choices)
        if abort:
            choices_all.append(abort)

        for i, choice in enumerate(choices_all):
            lines.append(
                PromptResponseLine(
                    segments=[
                        PromptResponseSegment(
                            text=f"  {i + 1}. → ",
                            color=TerminalColor.CYAN,
                            styles=[TextStyle.DIM]
                        ),
                        PromptResponseSegment(
                            text=choice,
                            color=TerminalColor.WHITE,
                        ),
                    ]
                )
            )

        return cls(
            lines=lines,
            choices=choices_all,
            default=default,
            question=question,
            verbosity=verbosity,
        )

    def ask(self):
        import readchar
        idx = 0

        while True:
            print("\033c", end="")
            if self.question is not None:
                print(f"{self.question}:\n")

            for i, opt in enumerate(self.choices):
                if i == idx:
                    print(f"> {TerminalColor.BLUE}{opt}{TerminalColor.RESET}")
                else:
                    print(f"  {opt}")

            key = readchar.readkey()
            if key == readchar.key.UP:
                idx = (idx - 1) % len(self.choices)
            elif key == readchar.key.DOWN:
                idx = (idx + 1) % len(self.choices)
            elif key in (readchar.key.ENTER, "\r", "\n"):
                return self.choices[idx]

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        from wexample_prompt.example.response.interactive.choice_example import ChoiceExample
        return ChoiceExample
