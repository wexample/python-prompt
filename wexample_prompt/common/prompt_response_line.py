"""Prompt response line implementation."""
from typing import List, Optional, TYPE_CHECKING

from pydantic import Field

from wexample_helpers.classes.extended_base_model import ExtendedBaseModel
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment

if TYPE_CHECKING:
    from wexample_prompt.enums.terminal_color import TerminalColor


class PromptResponseLine(ExtendedBaseModel):
    """A line of text composed of one or more segments with optional styling and layout."""

    segments: List[PromptResponseSegment] = Field(
        default_factory=list,
        description="List of text segments that constitute a line"
    )

    @classmethod
    def create_from_string(cls, text: str, color: Optional["TerminalColor"] = None) -> "PromptResponseLine":
        """
            Create a line from a single text string.
        """
        return cls(
            segments=[
                PromptResponseSegment(
                    text=text,
                    color=color
                )
            ]
        )

    def render(self, context: PromptContext) -> str:
        """Render the line within the context width, wrapping segments as needed.
        """
        indentation = context.render_indentation()
        max_content_width = max(0, (context.width or 0) - self._visible_len(indentation)) if context.width else None

        if not max_content_width:
            rendered_segments = []
            for seg in self.segments:
                rendered, _ = seg.render(context, line_remaining_width=10 ** 9)
                rendered_segments.append(rendered)
            return f"{indentation}{''.join(rendered_segments)}"

        lines: list[str] = []
        current_line = ""
        remaining = max_content_width

        queue = list(self.segments)
        carry_over: Optional[PromptResponseSegment] = None

        while queue or carry_over:
            if carry_over is not None:
                rendered, remainder = carry_over.render(context, remaining)
                current_line += rendered
                remaining -= self._visible_len(rendered)
                carry_over = remainder
            else:
                seg = queue.pop(0)
                rendered, remainder = seg.render(context, remaining)
                current_line += rendered
                remaining -= self._visible_len(rendered)
                carry_over = remainder

            if remaining <= 0 or (carry_over is not None and remaining == 0):
                lines.append(f"{indentation}{current_line}")
                current_line = ""
                remaining = max_content_width
                continue

            if carry_over is None and not queue:
                lines.append(f"{indentation}{current_line}")
                current_line = ""
                remaining = max_content_width

        if current_line:
            lines.append(f"{indentation}{current_line}")

        return "\n".join(lines)

    def _visible_len(self, s: str) -> int:
        from wexample_helpers.helpers.ansi import ansi_strip

        return len(ansi_strip(s))
