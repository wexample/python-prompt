"""Confirmation dialog interactive response (box style)."""
from typing import Any, Dict, Optional, Tuple, Type, ClassVar

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

    # Preset mappings (key -> (value, label))
    MAPPING_PRESET_YES_NO: ClassVar[Dict[str, Tuple[str, str]]] = {
        "y": ("yes", "Yes"),
        "n": ("no", "No"),
    }
    MAPPING_PRESET_OK_CANCEL: ClassVar[Dict[str, Tuple[str, str]]] = {
        "y": ("ok", "Ok"),
        "n": ("cancel", "Cancel"),
    }
    MAPPING_PRESET_YES_NO_ALL: ClassVar[Dict[str, Tuple[str, str]]] = {
        "y": ("yes", "Yes"),
        "Y": ("yes_all", "Yes for all"),
        "n": ("no", "No"),
    }
    MAPPING_PRESET_CONTINUE_CANCEL: ClassVar[Dict[str, Tuple[str, str]]] = {
        "y": ("continue", "Continue"),
        "n": ("cancel", "Cancel"),
    }

    question: str = Field(
        default="Please confirm:",
        description="The question to ask to the user"
    )
    width: Optional[int] = Field(
        default=None,
        description="Total width of the box (in characters). If None, uses context width or content width."
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
            choices: Optional[Dict[str, Tuple[str, str]]] = None,
            default: Optional[str] = None,
            width: Optional[int] = None,
            verbosity: VerbosityLevel = VerbosityLevel.DEFAULT,
            reset_on_finish: bool = False,
    ) -> "ConfirmPromptResponse":
        """Create a confirmation dialog with explicit key mappings.

        choices expects a mapping of key -> (value, label).
        If not provided, defaults to MAPPING_PRESET_YES_NO for convenience.
        """
        mapping: Dict[str, Tuple[str, str]] = choices or cls.MAPPING_PRESET_YES_NO

        return cls(
            question=question,
            options=mapping,
            default_value=default,
            width=width,
            reset_on_finish=reset_on_finish,
            verbosity=verbosity,
            # allow_abort is True by default; ESC/q return None
        )

    def _build_lines(self, context: "PromptContext") -> None:
        # Compute box width: prefer explicit width, else context width, else content-based with a floor
        width = context.get_width()

        # Build options text in the order provided by the mapping (insertion order)
        parts: list[tuple[str, str, str]] = []  # (key, value, label)
        for k, (v, label) in self.options.items():
            parts.append((k, v, label))
        options_text = " / ".join([f"[{k}: {label}]" for k, _, label in parts])

        content_width = max(len(self.question), len(options_text))
        min_width = max(45, content_width + 4)
        box_width = max(self.width or 0, width or 0, min_width)

        def center(s: str) -> str:
            return s.center(box_width)

        # Compose a boxed layout using lines and segments
        self.lines = []
        horiz = "-" * box_width
        # top border
        self.lines.append(PromptResponseLine(segments=[PromptResponseSegment(text=horiz, color=TerminalColor.WHITE)]))
        # empty line
        self.lines.append(
            PromptResponseLine(segments=[PromptResponseSegment(text=center(""), color=TerminalColor.RESET)]))
        # question line centered
        self.lines.append(
            PromptResponseLine(
                segments=[
                    PromptResponseSegment(
                        text=center(self.question),
                        color=TerminalColor.LIGHT_WHITE,
                        styles=[TextStyle.BOLD],
                    ),
                ]
            )
        )
        # empty line
        self.lines.append(
            PromptResponseLine(segments=[PromptResponseSegment(text=center(""), color=TerminalColor.RESET)]))
        # options line centered; highlight default_value if set
        left_pad = max((box_width - len(options_text)) // 2, 0)
        option_segments: list[PromptResponseSegment] = []
        if left_pad:
            option_segments.append(PromptResponseSegment(text=(" " * left_pad), color=TerminalColor.RESET))
        for idx, (k, v, label) in enumerate(parts):
            text = f"[{k}: {label}]"
            if self.default_value is not None and v == self.default_value:
                option_segments.append(
                    PromptResponseSegment(text=text, color=TerminalColor.LIGHT_WHITE, styles=[TextStyle.BOLD])
                )
            else:
                option_segments.append(
                    PromptResponseSegment(text=text, color=TerminalColor.WHITE)
                )
            if idx < len(parts) - 1:
                option_segments.append(PromptResponseSegment(text=" / ", color=TerminalColor.WHITE))

        self.lines.append(PromptResponseLine(segments=option_segments))
        # empty line
        self.lines.append(
            PromptResponseLine(segments=[PromptResponseSegment(text=center(""), color=TerminalColor.RESET)]))
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
            self._build_lines(context=context)
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
