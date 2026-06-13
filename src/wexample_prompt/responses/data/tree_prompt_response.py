"""Tree response implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.common.prompt_response_line import PromptResponseLine
    from wexample_prompt.enums.verbosity_level import VerbosityLevel


@base_class
class TreePromptResponse(AbstractPromptResponse):
    """Response for displaying hierarchical data in a tree structure."""

    branch_style: str = public_field(
        default="├", description="The character used to render branch"
    )
    dash_style: str = public_field(
        default="──", description="The character used to render dash"
    )
    data: dict[str, Any] = public_field(description="The data to display")
    leaf_style: str = public_field(
        default="└", description="The character used to render leaf"
    )
    pipe_style: str = public_field(
        default="│", description="The character used to render pipe"
    )

    @classmethod
    def create_tree(
        cls,
        data: dict[str, Any],
        verbosity: VerbosityLevel | None = None,
    ) -> TreePromptResponse:
        return cls(
            lines=[],
            data=data,
            verbosity=verbosity,
        )

    @classmethod
    def get_example_class(cls) -> type:
        from wexample_prompt.example.response.data.tree_example import TreeExample

        return TreeExample

    def render(self, context: PromptContext | None = None) -> str | None:
        from wexample_prompt.common.prompt_response_line import PromptResponseLine
        from wexample_prompt.common.prompt_response_segment import PromptResponseSegment

        if not self.data:
            return ""

        lines: list[PromptResponseLine] = []
        lines.append(PromptResponseLine(segments=[PromptResponseSegment(text="")]))

        self._build_tree(self.data, "", lines)

        lines.append(PromptResponseLine(segments=[PromptResponseSegment(text="")]))
        self.lines = lines
        return super().render(context=context)

    def _build_tree(
        self, data: dict[str, Any], prefix: str, lines: list[PromptResponseLine]
    ) -> None:
        from wexample_prompt.common.prompt_response_line import PromptResponseLine
        from wexample_prompt.common.prompt_response_segment import PromptResponseSegment

        items = list(data.items())
        last_idx = len(items) - 1
        _leaf = self.leaf_style
        _branch = self.branch_style
        _dash = self.dash_style
        _pipe = self.pipe_style
        for i, (key, value) in enumerate(items):
            is_last = i == last_idx
            current_prefix = f"{_leaf}{_dash} " if is_last else f"{_branch}{_dash} "

            # Parse key for inline formatting
            from wexample_prompt.common.style_markup_parser import flatten_style_markup

            key_segments = flatten_style_markup(key, joiner=None)

            # Prepend prefix and tree symbols
            all_segments = [
                PromptResponseSegment(text=f"{prefix}{current_prefix}")
            ] + key_segments
            lines.append(PromptResponseLine(segments=all_segments))

            next_prefix = prefix + ("    " if is_last else f"{_pipe}   ")
            if isinstance(value, dict):
                self._build_tree(value, next_prefix, lines)
            elif value is not None:
                # Parse value for inline formatting
                value_segments = flatten_style_markup(str(value), joiner=None)

                # Prepend prefix and tree symbols
                all_value_segments = [
                    PromptResponseSegment(text=f"{next_prefix}{_leaf}{_dash} ")
                ] + value_segments
                lines.append(PromptResponseLine(segments=all_value_segments))
