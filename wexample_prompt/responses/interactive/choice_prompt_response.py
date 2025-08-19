from typing import Any, List, Optional, Dict, Type, TYPE_CHECKING, Union, Mapping

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
        description="Default selected value for the prompt (matched against Choice.value, title, or index)"
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
        description="The line that displays the question"
    )

    @classmethod
    def create_choice(
            cls,
            question: str,
            choices: Union[List[Any], Mapping[Any, Any]],
            default: Optional[Any] = None,
            abort: Optional[bool | str] = None,
            color: Optional[TerminalColor] = None,
            verbosity: VerbosityLevel = VerbosityLevel.DEFAULT
    ) -> "ChoicePromptResponse":
        """Factory to create a ChoicePromptResponse."""

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

        # Build choices from list or mapping
        if isinstance(choices, Mapping):
            for key, title in choices.items():
                choices_list.append(
                    Choice(
                        value=key,
                        title=str(title),
                        line=PromptResponseLine(segments=[]),
                    )
                )
        else:
            for item in choices:
                choices_list.append(
                    Choice(
                        value=item,
                        title=str(item),
                        line=PromptResponseLine(segments=[]),
                    )
                )

        # Add abort option if requested.
        if abort is not False:
            choices_list.append(
                Choice(
                    value=ChoiceValue.ABORT,
                    title=str(abort if abort is not None else "Abort"),
                    line=PromptResponseLine(segments=[]),
                )
            )

        return cls(
            question_line=question_line,
            choices=choices_list,
            default=default,
            question=question,
            verbosity=verbosity,
        )

    def ask(self, context: Optional["PromptContext"] = None) -> Optional[str | int]:
        """Render the prompt and return the selected value."""
        import readchar

        from wexample_prompt.common.prompt_context import PromptContext
        context = PromptContext.create_if_none(context=context)
        # Disable formatting to avoid creating new lines
        context.formatting = False

        if not self.choices:
            # Nothing to choose from
            return None

        # Resolve default index (match by value, title, or integer index)
        def _resolve_default_index() -> int:
            if self.default is None:
                return 0
            try:
                # If an index is provided
                if isinstance(self.default, int):
                    return max(0, min(self.default, len(self.choices) - 1))
                # Match by value or title
                for i, c in enumerate(self.choices):
                    if c.value == self.default or str(c.title) == str(self.default):
                        return i
            except Exception:
                pass
            return 0

        idx = _resolve_default_index()
        printed_lines = 0  # how many lines we printed last frame

        while True:
            # Clear only our previous render block (not the whole screen)
            if printed_lines > 0:
                # Move cursor up 'printed_lines' and clear to end of screen
                # \033[{n}F moves to the beginning of the n-th previous line
                # \033[J clears from cursor to end of screen
                print(f"\033[{printed_lines}F\033[J", end="")

            # Rebuild lines for this frame
            self.lines = [self.question_line]

            for i, choice in enumerate(self.choices):
                line = choice.line

                is_selected = (i == idx)
                is_abort = (choice.value == ChoiceValue.ABORT)

                # Prefix: no numbering, use chevron only for non-abort selected.
                if is_abort:
                    prefix = "  ⨯ "
                    prefix_color = TerminalColor.WHITE
                    prefix_styles = []
                else:
                    prefix = "  › " if is_selected else "    "
                    prefix_color = TerminalColor.LIGHT_WHITE if is_selected else TerminalColor.RESET
                    prefix_styles = [TextStyle.BOLD] if is_selected else []

                # Title styling
                title_color = TerminalColor.LIGHT_WHITE if is_selected else TerminalColor.RESET
                title_styles = [TextStyle.BOLD] if is_selected else []

                line.segments = [
                    PromptResponseSegment(
                        text=prefix,
                        color=prefix_color,
                        styles=prefix_styles,
                    ),
                    PromptResponseSegment(
                        text=str(choice.title),
                        color=title_color,
                        styles=title_styles,
                    ),
                ]

                self.lines.append(line)

            # Controls helper footer (in white)
            controls_line = PromptResponseLine(
                segments=[
                    PromptResponseSegment(
                        text="\nUse ↑/↓ to navigate • Enter to select • Esc or q to abort",
                        color=TerminalColor.WHITE,
                        styles=[],
                    )
                ]
            )
            self.lines.append(controls_line)

            rendered = self.render(context=context)
            print(rendered)
            # Count how many lines we just printed to clear them next frame
            printed_lines = rendered.count("\n") + 1

            key = readchar.readkey()
            if key == readchar.key.UP:
                idx = (idx - 1) % len(self.choices)
            elif key == readchar.key.DOWN:
                idx = (idx + 1) % len(self.choices)
            elif key in (readchar.key.ENTER, "\r", "\n"):
                selected = self.choices[idx]
                if selected.value == ChoiceValue.ABORT:
                    return None
                return selected.value
            elif key in (readchar.key.ESC, "q", "Q"):
                # Quick abort with ESC or q/Q
                return None

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        from wexample_prompt.example.response.interactive.choice_example import ChoiceExample
        return ChoiceExample
