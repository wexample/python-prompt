"""Response for displaying suggestions with optional descriptions."""
from typing import List, Optional, Type

from pydantic import Field

from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.enums.text_style import TextStyle
from wexample_prompt.common.color_manager import ColorManager
from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse


class SuggestionsPromptResponse(AbstractPromptResponse):
    """Display a list of suggestions with an introductory message."""

    message: str = Field(description="The message to display above suggestions")
    suggestions: List[str] = Field(default_factory=list, description="The suggestions list")
    arrow_style: str = Field(default="→", description="Bullet/arrow prefix for each suggestion")

    @classmethod
    def get_example_class(cls) -> Type:
        from wexample_prompt.example.response.data.suggestions_example import SuggestionsExample
        return SuggestionsExample

    @classmethod
    def create_suggestions(
        cls,
        message: str,
        suggestions: List[str],
        arrow_style: str = "→",
        verbosity: VerbosityLevel = VerbosityLevel.DEFAULT,
    ) -> "SuggestionsPromptResponse":
        return cls(
            lines=[],
            message=message,
            suggestions=suggestions,
            arrow_style=arrow_style,
            verbosity=verbosity,
        )

    def render(self, context=None) -> Optional[str]:
        lines: List[PromptResponseLine] = []
        # Top spacer
        lines.append(PromptResponseLine(segments=[PromptResponseSegment(text="")]))

        # Message line
        lines.append(
            PromptResponseLine(
                segments=[
                    PromptResponseSegment(
                        text=ColorManager.colorize(f"{self.message}:", TerminalColor.BLUE),
                        styles=[TextStyle.BOLD],
                    )
                ]
            )
        )

        # Suggestions
        for suggestion in self.suggestions:
            lines.append(
                PromptResponseLine(
                    segments=[
                        PromptResponseSegment(
                            text=ColorManager.colorize(f"  {self.arrow_style} ", TerminalColor.CYAN),
                            styles=[TextStyle.BOLD],
                        ),
                        PromptResponseSegment(text=suggestion),
                    ]
                )
            )

        # Bottom spacer
        lines.append(PromptResponseLine(segments=[PromptResponseSegment(text="")]))

        self.lines = lines
        return super().render(context=context)
