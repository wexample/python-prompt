from typing import Any, List, Optional, Dict, Type, TYPE_CHECKING, Union, Mapping

from pydantic import Field

from wexample_prompt.common.choice.choice import Choice
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.const.types import LineMessage
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
    question: LineMessage = Field(
        default=None,
        description="Question text shown to the user"
    )
    question_lines: List["PromptResponseLine"] = Field(
        description="Rendered question lines"
    )
    predefined_answer: Any = Field(
        default=None,
        description="The answer of the question, in order to make the response non interactive"
    )

    @classmethod
    def create_choice(
            cls,
            question: LineMessage,
            choices: Union[List[Any], Mapping[Any, Any]],
            default: Optional[Any] = None,
            abort: Optional[bool | str] = None,
            color: Optional[TerminalColor] = None,
            reset_on_finish: bool = False,
            predefined_answer: Any = None,
            verbosity: VerbosityLevel = VerbosityLevel.DEFAULT
    ) -> "ChoicePromptResponse":
        """Factory to create a ChoicePromptResponse."""
        # Build question lines from LineMessage, apply styles/colors on segments
        question_lines = PromptResponseLine.create_from_string(question, color=color)

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
            question_lines=question_lines,
            choices=choices_list,
            default=default,
            question=question,
            verbosity=verbosity,
            reset_on_finish=reset_on_finish,
            predefined_answer=predefined_answer,
        )

    def render(self, context: Optional["PromptContext"] = None) -> None:
        """Render the prompt and return the selected value."""
        import readchar

        from wexample_prompt.common.prompt_context import PromptContext
        context = PromptContext.create_if_none(context=context)

        if not self.choices:
            # Nothing to choose from
            self._answer = None
            return

        # Resolve index for a target (match by value, title, or integer index)
        def _resolve_index_for(target: Any) -> int:
            if target is None:
                return 0
            try:
                if isinstance(target, int):
                    return max(0, min(target, len(self.choices) - 1))
                for i, c in enumerate(self.choices):
                    if c.value == target or str(c.title) == str(target):
                        return i
            except Exception:
                pass
            return 0

        # Preselect default or injected answer for the first render
        idx = _resolve_index_for(self.predefined_answer if self.predefined_answer is not None else self.default)
        printed_lines = 0  # how many lines we printed last frame

        while True:
            # Clear only our previous render block (not the whole screen)
            self._partial_clear(printed_lines)

            # Rebuild lines for this frame (all question lines first)
            self.lines = self.question_lines

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
                        text="Use ↑/↓ to navigate • Enter to select • Esc or q to abort",
                        color=TerminalColor.WHITE,
                        styles=[],
                    )
                ]
            )
            self.lines.append(controls_line)

            # Render and print this frame
            printed_lines = self._print_render(context=context)

            # If an answer is injected (non-interactive mode), return it as-is
            if self.predefined_answer is not None:
                if self.reset_on_finish and printed_lines > 0:
                    self._partial_clear(printed_lines)
                self._answer = self.predefined_answer
                return

            key = self._read_key()
            if key == readchar.key.UP:
                idx = (idx - 1) % len(self.choices)
            elif key == readchar.key.DOWN:
                idx = (idx + 1) % len(self.choices)
            elif key in (readchar.key.ENTER, "\r", "\n"):
                selected = self.choices[idx]
                if selected.value == ChoiceValue.ABORT:
                    if self.reset_on_finish and printed_lines > 0:
                        self._partial_clear(printed_lines)
                    self._answer = None
                    return
                if self.reset_on_finish and printed_lines > 0:
                    self._partial_clear(printed_lines)
                self._answer = selected.value
                return
            elif key in (readchar.key.ESC, "q", "Q"):
                # Quick abort with ESC or q/Q
                if self.reset_on_finish and printed_lines > 0:
                    self._partial_clear(printed_lines)
                self._answer = None
                return

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        from wexample_prompt.example.response.interactive.choice_example import ChoiceExample
        return ChoiceExample
