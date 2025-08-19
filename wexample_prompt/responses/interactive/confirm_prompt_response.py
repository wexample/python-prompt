"""Confirmation dialog interactive response (box style)."""
from typing import Any, Dict, Optional, Tuple, Type

from pydantic import Field

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.enums.text_style import TextStyle
from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.responses.interactive.abstract_interactive_prompt_response import (
    AbstractInteractivePromptResponse,
)


class ConfirmPromptResponse(AbstractInteractivePromptResponse):
    """Confirmation dialog with a boxed layout and keyboard shortcuts."""

    question: str = Field(
        default="Please confirm:",
        description="The question to ask to the user"
    )
    # Map pressed key -> (value, label)
    options: Dict[str, Tuple[str, str]] = Field(
        default_factory=dict,
        description="Keyboard shortcuts mapping to (return value, display label)",
    )
    default_value: Optional[str] = Field(
        default=None,
        description="The value to return when quitting"
    )
    allow_abort: bool = Field(default=True, description="ESC/q aborts and returns None when allowed.")

    @classmethod
    def get_example_class(cls) -> Type:
        from wexample_prompt.example.response.interactive.confirm_example import ConfirmExample
        return ConfirmExample

    @classmethod
    def create_confirm(
            cls,
            question: str = "Please confirm:",
            preset: Optional[str] = None,
            choices: Optional[Dict[str, str]] = None,
            default: Optional[str] = None,
            verbosity: VerbosityLevel = VerbosityLevel.DEFAULT,
            reset_on_finish: bool = False,
    ) -> "ConfirmPromptResponse":
        """Create a confirmation dialog configured either by preset or explicit choices."""
        mapping: Dict[str, Tuple[str, str]]
        if choices is not None:
            # Heuristic: map y to first key, n to second, Y to third if present
            items = list(choices.items())
            mapping = {}
            if len(items) >= 1:
                mapping["y"] = (items[0][0], items[0][1])
            if len(items) >= 2:
                mapping["n"] = (items[1][0], items[1][1])
            if len(items) >= 3:
                mapping["Y"] = (items[2][0], items[2][1])
        else:
            preset = preset or "yes_no"
            if preset == "yes_no":
                mapping = {"y": ("yes", "Yes"), "n": ("no", "No")}
            elif preset == "ok_cancel":
                mapping = {"y": ("ok", "Ok"), "n": ("cancel", "Cancel")}
            elif preset == "yes_no_all":
                mapping = {"y": ("yes", "Yes"), "Y": ("yes_all", "Yes for all"), "n": ("no", "No")}
            elif preset == "continue_cancel":
                mapping = {"y": ("continue", "Continue"), "n": ("cancel", "Cancel")}
            else:
                raise ValueError(f"Unknown confirm preset: {preset}")

        return cls(
            question=question,
            options=mapping,
            default_value=default,
            reset_on_finish=reset_on_finish,
            verbosity=verbosity,
            # allow_abort is True by default; ESC/q return None
        )

    def _build_lines(self) -> None:
        # Compose a boxed layout using lines and segments
        self.lines = []
        horiz = "-" * max(45, len(self.question) + 8)
        # top border
        self.lines.append(PromptResponseLine(segments=[PromptResponseSegment(text=horiz, color=TerminalColor.WHITE)]))
        # empty line
        self.lines.append(PromptResponseLine(segments=[PromptResponseSegment(text="", color=TerminalColor.RESET)]))
        # question line (indented and bold)
        self.lines.append(
            PromptResponseLine(
                segments=[
                    PromptResponseSegment(text="        ", color=TerminalColor.RESET),
                    PromptResponseSegment(text=self.question, color=TerminalColor.LIGHT_WHITE, styles=[TextStyle.BOLD]),
                ]
            )
        )
        # empty line
        self.lines.append(PromptResponseLine(segments=[PromptResponseSegment(text="", color=TerminalColor.RESET)]))

        # options line
        parts = []
        # Stable order: y, Y, n, then others
        order = [k for k in ["y", "Y", "n"] if k in self.options]
        order += [k for k in self.options.keys() if k not in order]
        for k in order:
            val, label = self.options[k]
            parts.append(f"[{k}: {label}]")
        options_text = " / ".join(parts)
        self.lines.append(
            PromptResponseLine(
                segments=[
                    PromptResponseSegment(text="  ", color=TerminalColor.RESET),
                    PromptResponseSegment(text=options_text, color=TerminalColor.WHITE),
                ]
            )
        )
        # empty line
        self.lines.append(PromptResponseLine(segments=[PromptResponseSegment(text="", color=TerminalColor.RESET)]))
        # bottom border
        self.lines.append(PromptResponseLine(segments=[PromptResponseSegment(text=horiz, color=TerminalColor.WHITE)]))

    def ask(self, context: Optional["PromptContext"] = None, answer: Any = None) -> Optional[str]:
        from wexample_prompt.common.prompt_context import PromptContext
        context = PromptContext.create_if_none(context=context)
        context.formatting = False

        printed = 0
        # render once per frame until a valid key or injected answer
        while True:
            self._partial_clear(printed)
            self._build_lines()
            printed = self._print_render(context=context)

            if answer is not None:
                if self.reset_on_finish and printed > 0:
                    self._partial_clear(printed)
                return str(answer)

            key = self._read_key()
            # normalize single-char keys for mapping
            if key in self.options:
                value, _ = self.options[key]
                if self.reset_on_finish and printed > 0:
                    self._partial_clear(printed)
                return value
            elif key in ("\r", "\n") and self.default_value is not None:
                if self.reset_on_finish and printed > 0:
                    self._partial_clear(printed)
                return self.default_value
            elif key in ("\x1b", "q", "Q") and self.allow_abort:
                if self.reset_on_finish and printed > 0:
                    self._partial_clear(printed)
                return None
