from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.common.prompt_response_line import PromptResponseLine
    from wexample_prompt.enums.verbosity_level import VerbosityLevel


@base_class
class PropertiesPromptResponse(AbstractPromptResponse):
    """Render a dictionary of properties as a formatted block, with optional title.

    The visual width adapts to the provided render context. Lines are generated during
    render, so the response remains context-agnostic until displayed.
    """

    nested_indent: int = public_field(
        default=2,
        description="Indentation inside the properties list, when rendering sub list of items",
    )
    properties: dict[str, Any] = public_field(
        factory=dict, description="The list of properties to display"
    )
    title: str | None = public_field(
        default=None, description="The title of the properties list"
    )

    @classmethod
    def create_properties(
        cls,
        properties: dict[str, Any],
        title: str | None = None,
        nested_indent: int = 2,
        verbosity: VerbosityLevel | None = None,
    ) -> PropertiesPromptResponse:
        return cls(
            lines=[],  # Lines will be built in render() because we neet context with to create them.
            properties=properties,
            title=title,
            nested_indent=nested_indent,
            verbosity=verbosity,
        )

    @classmethod
    def get_example_class(cls) -> type:
        from wexample_prompt.example.response.data.properties_example import (
            PropertiesExample,
        )

        return PropertiesExample

    @staticmethod
    def _wrap_long_rows(content_lines: list[str], max_inner_width: int) -> list[str]:
        """Word-wrap "{key} : {value}" rows wider than `max_inner_width`.

        Continuation lines are padded so they line up with the value column,
        which keeps the property/value grid readable even when one value
        spans several rows. Lines without a " : " separator (nested-dict
        headers) are left untouched.
        """
        import textwrap

        from wexample_prompt.helper.terminal import terminal_get_visible_width

        wrapped: list[str] = []
        for line in content_lines:
            if terminal_get_visible_width(line) <= max_inner_width:
                wrapped.append(line)
                continue

            sep_idx = line.find(" : ")
            if sep_idx == -1:
                wrapped.append(line)
                continue

            prefix = line[: sep_idx + 3]
            value = line[sep_idx + 3 :]
            prefix_visible = terminal_get_visible_width(prefix)
            wrap_width = max(1, max_inner_width - prefix_visible)

            chunks = textwrap.wrap(
                value,
                width=wrap_width,
                break_long_words=True,
                break_on_hyphens=False,
                drop_whitespace=True,
                replace_whitespace=False,
            ) or [""]

            wrapped.append(prefix + chunks[0])
            indent = " " * prefix_visible
            for chunk in chunks[1:]:
                wrapped.append(indent + chunk)
        return wrapped

    @staticmethod
    def _format_properties(
        properties: dict[str, Any],
        key_width: int,
        indent: int,
        current_indent: int = 0,
    ) -> list[str]:
        lines: list[str] = []
        indent_str = " " * current_indent
        for key, value in properties.items():
            if isinstance(value, dict):
                lines.append(f"{indent_str}{str(key)}:")
                lines.extend(
                    PropertiesPromptResponse._format_properties(
                        value, key_width, indent, current_indent + indent
                    )
                )
            else:
                key_str = str(key).ljust(key_width)
                lines.append(f"{indent_str}{key_str} : {str(value)}")
        return lines

    def render(self, context: PromptContext | None = None) -> str | None:
        """Render the properties into lines using the provided context width."""
        from wexample_prompt.common.prompt_context import PromptContext
        from wexample_prompt.common.prompt_response_line import PromptResponseLine
        from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
        from wexample_prompt.common.style_markup_parser import flatten_style_markup
        from wexample_prompt.helper.terminal import terminal_get_visible_width

        if not self.properties:
            return ""

        context = PromptContext.create_if_none(context=context)

        max_key_width = 0

        def scan_keys(obj: dict[str, Any]) -> None:
            nonlocal max_key_width
            for k, v in obj.items():
                max_key_width = max(max_key_width, len(str(k)))
                if isinstance(v, dict):
                    scan_keys(v)

        scan_keys(self.properties)

        content_lines = self._format_properties(
            self.properties, max_key_width, self.nested_indent
        )

        bordered = context.bordered

        # Cap content to terminal width so the box never overflows. The full
        # cartouche occupies `inner_width + 4` columns (│ + space + content +
        # space + │), so the inner area can grow up to terminal_width - 4.
        target_width = context.get_available_width() if bordered else 0
        max_inner_width = max(1, target_width - 4) if target_width else 0

        # Wrap rows whose value exceeds the box's usable inner width. The
        # wrap aligns continuation lines to the value column (right after
        # "{key} : ") so the property/value relationship stays visually
        # clear and the box keeps a tidy grid.
        if max_inner_width:
            content_lines = self._wrap_long_rows(content_lines, max_inner_width)

        lines: list[PromptResponseLine] = []

        # Flatten markup once per line so visible-width math uses what will
        # actually be rendered, not the raw `@color{}` source.
        flattened = [flatten_style_markup(line, joiner=None) for line in content_lines]
        content_visible_widths = [
            sum(terminal_get_visible_width(seg.text) for seg in segs)
            for segs in flattened
        ]

        if bordered:
            # Box is sized to content (like TablePromptResponse), not to the
            # full terminal width — visually consistent with the table cartouche.
            max_content = max(content_visible_widths, default=0)
            # Title needs "╭─ <title> ─╮" = 4 extra chars beyond title length.
            title_min = (len(self.title) + 4) if self.title else 0
            inner_width = max(max_content, title_min, 1)
            if max_inner_width:
                inner_width = min(inner_width, max_inner_width)
            box_width = inner_width + 2  # leading + trailing space inside │ … │

            # Leading blank for visual separation (consistent with table).
            lines.append(PromptResponseLine(segments=[PromptResponseSegment(text="")]))

            if self.title:
                # ╭─ Title ─…─╮ : 3 chars consumed by "╭─ " + " ", rest is fill before ╮.
                fill = max(0, box_width - 3 - len(self.title))
                lines.append(
                    PromptResponseLine(
                        segments=[
                            PromptResponseSegment(
                                text="╭─ " + self.title + " " + "─" * fill + "╮"
                            )
                        ]
                    )
                )
            else:
                lines.append(
                    PromptResponseLine(
                        segments=[
                            PromptResponseSegment(text="╭" + "─" * box_width + "╮")
                        ]
                    )
                )

            for content_segments, visible in zip(flattened, content_visible_widths):
                padding = max(0, inner_width - visible)
                lines.append(
                    PromptResponseLine(
                        segments=[
                            PromptResponseSegment(text="│ "),
                            *content_segments,
                            PromptResponseSegment(text=" " * padding + " │"),
                        ]
                    )
                )

            lines.append(
                PromptResponseLine(
                    segments=[
                        PromptResponseSegment(text="╰" + "─" * box_width + "╯")
                    ]
                )
            )
        else:
            # Naked mode: no box at all (used when wrapped in a frame, which
            # already provides its own cartouche).
            if self.title:
                lines.append(
                    PromptResponseLine(
                        segments=[PromptResponseSegment(text=self.title)]
                    )
                )
            for content_segments in flattened:
                lines.append(PromptResponseLine(segments=content_segments))

        # Replace and delegate to base to apply verbosity and segment rendering
        self.lines = lines
        return super().render(context=context)
