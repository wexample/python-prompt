from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.enums.terminal_color import TerminalColor
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.example.abstract_response_example import (
        AbstractResponseExample,
    )


@base_class
class FramePromptResponse(AbstractPromptResponse):
    """Render content inside a rounded-corner frame (like the `claude` CLI cartouche).

    Accepts either raw `text` or nested `responses`. When nested responses are
    provided, each is rendered first and its rendered string is wrapped line by
    line with the frame characters — content can therefore contain ANSI codes.
    """

    border_color: "TerminalColor | None" = public_field(
        default=None,
        description="Color applied to the frame border characters",
    )
    padding: int = public_field(
        default=1,
        description="Horizontal padding (number of spaces) between border and content",
    )
    responses: list[AbstractPromptResponse] = public_field(
        factory=list,
        description="Inner responses to render inside the frame",
    )
    text: str | list[str] | None = public_field(
        default=None,
        description="Convenience raw text content (string or list of lines)",
    )
    title: str | None = public_field(
        default=None,
        description="Optional title rendered inline in the top border",
    )

    @classmethod
    def create_frame(
        cls,
        text: str | list[str] | None = None,
        responses: list[AbstractPromptResponse] | None = None,
        title: str | None = None,
        border_color: "TerminalColor | None" = None,
        padding: int = 1,
        verbosity: "VerbosityLevel | None" = None,
    ) -> FramePromptResponse:
        return cls(
            lines=[],
            text=text,
            responses=list(responses) if responses else [],
            title=title,
            border_color=border_color,
            padding=max(0, padding),
            verbosity=verbosity,
        )

    @classmethod
    def get_example_class(cls) -> type[AbstractResponseExample]:
        from wexample_prompt.example.response.frame_example import FrameExample

        return FrameExample

    def render(self, context: "PromptContext | None" = None) -> str | None:
        from wexample_helpers.helpers.ansi import ansi_display_width
        from wexample_prompt.common.color_manager import ColorManager
        from wexample_prompt.common.prompt_context import PromptContext

        context = PromptContext.create_if_none(context=context)

        if not self._verbosity_context_allows_display(context=context):
            return None

        content_lines = self._collect_content_lines(context=context)

        total_width = context.get_width()
        indent_width = context.get_indentation_visible_width()
        # 2 corners + 2*padding minimum reserved for border/padding
        max_inner = max(1, total_width - indent_width - 2 - 2 * self.padding)

        content_widths = [ansi_display_width(line) for line in content_lines] or [0]
        inner_w = min(max(content_widths), max_inner)

        title = self.title
        if title:
            # Top border with title needs: corner + "─ " + title + " " + fill + corner
            # horizontal stretch (between corners) = 3 + len(title) + fill
            min_horiz_for_title = ansi_display_width(title) + 3
            inner_w = max(inner_w, min_horiz_for_title - 2 * self.padding)

        horiz_w = inner_w + 2 * self.padding

        colorize = (
            (lambda s: ColorManager.colorize(s, color=self.border_color))
            if context.colorized and self.border_color
            else (lambda s: s)
        )

        indent = context.render_indentation()

        out_lines: list[str] = []
        out_lines.append(indent + colorize(self._build_top(horiz_w)))
        for line in content_lines:
            out_lines.append(
                indent + self._build_middle(line, inner_w, colorize, ansi_display_width)
            )
        if not content_lines:
            out_lines.append(
                indent + self._build_middle("", inner_w, colorize, ansi_display_width)
            )
        out_lines.append(indent + colorize(self._build_bottom(horiz_w)))

        self._rendered_content = "\n".join(out_lines)
        return self._rendered_content

    def _build_bottom(self, horiz_w: int) -> str:
        return "╰" + ("─" * horiz_w) + "╯"

    def _build_middle(
        self,
        line: str,
        inner_w: int,
        colorize,
        width_fn,
    ) -> str:
        visible = width_fn(line)
        if visible > inner_w:
            from wexample_helpers.helpers.ansi import ansi_truncate_visible

            line = ansi_truncate_visible(line, inner_w)
            visible = inner_w
        pad_right = inner_w - visible
        pad = " " * self.padding
        return (
            colorize("│")
            + pad
            + line
            + (" " * pad_right)
            + pad
            + colorize("│")
        )

    def _build_top(self, horiz_w: int) -> str:
        if not self.title:
            return "╭" + ("─" * horiz_w) + "╮"
        # ╭─ Title ─...─╮  → between corners: "─ " + title + " " + fill
        from wexample_helpers.helpers.ansi import ansi_display_width

        title_w = ansi_display_width(self.title)
        fill = max(0, horiz_w - 3 - title_w)
        return "╭" + "─ " + self.title + " " + ("─" * fill) + "╮"

    def _collect_content_lines(self, context: "PromptContext") -> list[str]:
        lines: list[str] = []

        if self.responses:
            inner_context = self._build_inner_context(context)
            for response in self.responses:
                rendered = response.render(context=inner_context)
                if rendered is None:
                    continue
                # Inner indentation is added by the response itself; we wrap each output
                # line as-is so ANSI codes are preserved.
                for sub in rendered.split("\n"):
                    lines.append(sub)

        if self.text is not None:
            raw = [self.text] if isinstance(self.text, str) else list(self.text)
            for item in raw:
                lines.extend(item.split("\n"))

        return lines

    def _build_inner_context(self, context: "PromptContext") -> "PromptContext":
        from wexample_prompt.common.prompt_context import PromptContext

        kwargs = PromptContext.create_kwargs_from_context(context=context)
        # Inner content area: total width minus our own borders + padding
        outer = context.get_width() - context.get_indentation_visible_width()
        inner = max(1, outer - 2 - 2 * self.padding)
        kwargs["width"] = inner
        kwargs["indentation"] = 0
        kwargs["bordered"] = False
        return PromptContext.create_from_kwargs(kwargs=kwargs)
