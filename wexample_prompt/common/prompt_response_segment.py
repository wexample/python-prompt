from typing import TYPE_CHECKING, Optional, Tuple

from pydantic import Field

from wexample_helpers.classes.extended_base_model import ExtendedBaseModel
from wexample_prompt.enums.terminal_color import TerminalColor

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext


class PromptResponseSegment(ExtendedBaseModel):
    """A segment of text with optional styling."""
    text: str = Field(
        description="The content of the segment"
    )
    color: Optional[TerminalColor] = Field(
        default=None,
        description="The color to apply to segment on rendering, if allowed by context"
    )

    def render(self, context: "PromptContext", line_remaining_width: int) -> Tuple[str, Optional["PromptResponseSegment"]]:
        """Render the segment respecting the remaining width for the current line.

        Returns a tuple of (rendered_fit, remainder_segment).
        - rendered_fit: the rendered string (possibly colorized) that fits in the remaining width
        - remainder_segment: a new PromptResponseSegment with the leftover RAW text and same color, or None
        """
        # Split the RAW text by visible width first (no ANSI involved yet)
        fit_raw, remainder_raw = self._split_by_visible_width(self.text, line_remaining_width)

        # Colorize the part that fits (and the remainder will be colorized later when rendered on next line)
        rendered_fit = fit_raw
        if self.color and context.colorized and fit_raw:
            from wexample_prompt.common.color_manager import ColorManager
            rendered_fit = ColorManager.colorize(fit_raw, self.color)

        remainder_seg = None
        if remainder_raw:
            remainder_seg = PromptResponseSegment(text=remainder_raw, color=self.color)
        return rendered_fit, remainder_seg

    def _split_by_visible_width(self, text: str, width: int) -> Tuple[str, str]:
        """Split text so that the first part fits within `width` visible chars.

        Returns (fit, remainder). If width <= 0, fit is '', remainder is text.
        """
        if width <= 0 or not text:
            return "", text
        # Since text is raw (no ANSI), visible length equals len.
        if len(text) <= width:
            return text, ""
        return text[:width], text[width:]
