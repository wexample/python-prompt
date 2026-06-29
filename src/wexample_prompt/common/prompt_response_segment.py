from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.enums.text_style import TextStyle

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.enums.terminal_color import TerminalColor
    from wexample_prompt.enums.text_style import TextStyle


@base_class
class PromptResponseSegment(BaseClass):
    """A segment of text with optional styling."""

    color: TerminalColor | None = public_field(
        default=None,
        description="The color to apply to segment on rendering, if allowed by context",
    )
    styles: list[TextStyle] = public_field(
        factory=list,
        description="Optional text styles (bold, italic, underline, etc.) to apply when rendering",
    )
    text: str = public_field(description="The content of the segment")

    def __attrs_post_init__(self) -> None:
        if "\n" in self.text:
            raise ValueError(
                "Segment should not contain line breaks; use separate line objects instead"
            )

    def render(
        self, context: PromptContext, line_remaining_width: int
    ) -> tuple[str, PromptResponseSegment | None]:
        """Render the segment respecting the remaining width for the current line.

        Returns a tuple of (rendered_fit, remainder_segment).
        - rendered_fit: the rendered string (possibly colorized) that fits in the remaining width
        - remainder_segment: a new PromptResponseSegment with the leftover RAW text and same color, or None
        """
        from wexample_prompt.common.color_manager import ColorManager

        # Split the RAW text by visible width first (no ANSI involved yet)
        fit_raw, remainder_raw = self._split_by_visible_width(
            self.text, line_remaining_width
        )

        # Apply styles and color if allowed by context (single reset at the end)
        rendered_fit = fit_raw
        if context.colorized and fit_raw:

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

        Most segments hold raw text (no inline ANSI), so len() equals visible
        width and a byte-slice is correct. Some upstream renderers (e.g.
        Properties) pre-resolve `@color{}` markup to inline ANSI before
        building the segment, in which case len() over-counts. We probe the
        cheap len() path first and only escalate to `terminal_get_visible_width`
        when it might over-report — keeps the hot path on a single len().
        """
        if width <= 0 or not text:
            return "", text
        if len(text) <= width:
            return text, ""
        # len > width — either real overflow OR len inflated by inline ANSI.
        # Recompute against visible width to know which.
        from wexample_prompt.helper.terminal import terminal_get_visible_width

        if terminal_get_visible_width(text) <= width:
            return text, ""
        # True overflow on raw text: hard byte-slice (original behavior).
        return text[:width], text[width:]
