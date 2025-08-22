from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pydantic import Field
from wexample_helpers.classes.extended_base_model import ExtendedBaseModel
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.enums.text_style import TextStyle

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext


class PromptResponseSegment(ExtendedBaseModel):
    """A segment of text with optional styling."""

    text: str = Field(description="The content of the segment")
    color: TerminalColor | None = Field(
        default=None,
        description="The color to apply to segment on rendering, if allowed by context",
    )
    styles: list[TextStyle] = Field(
        default_factory=list,
        description="Optional text styles (bold, italic, underline, etc.) to apply when rendering",
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        if "\n" in self.text:
            raise ValueError(
                "Segment should not contain line breaks; use separate line objects instead"
            )

    def render(
        self, context: PromptContext, line_remaining_width: int
    ) -> tuple[str, Optional["PromptResponseSegment"]]:
        """Render the segment respecting the remaining width for the current line.

        Returns a tuple of (rendered_fit, remainder_segment).
        - rendered_fit: the rendered string (possibly colorized) that fits in the remaining width
        - remainder_segment: a new PromptResponseSegment with the leftover RAW text and same color, or None
        """
        # Split the RAW text by visible width first (no ANSI involved yet)
        fit_raw, remainder_raw = self._split_by_visible_width(
            self.text, line_remaining_width
        )

        # Apply styles and color if allowed by context (single reset at the end)
        rendered_fit = fit_raw
        if context.colorized and fit_raw:
            from wexample_prompt.common.color_manager import ColorManager

            prefix = ColorManager.build_prefix(color=self.color, styles=self.styles)
            if prefix:
                rendered_fit = f"{prefix}{fit_raw}\033[0m"

        remainder_seg = None
        if remainder_raw:
            remainder_seg = PromptResponseSegment(
                text=remainder_raw, color=self.color, styles=list(self.styles)
            )
        return rendered_fit, remainder_seg

    def _split_by_visible_width(self, text: str, width: int) -> tuple[str, str]:
        """Split text so that the first part fits within `width` visible chars.

        Returns (fit, remainder). If width <= 0, fit is '', remainder is text.
        """
        if width <= 0 or not text:
            return "", text
        # Since text is raw (no ANSI), visible length equals len.
        if len(text) <= width:
            return text, ""
        return text[:width], text[width:]
