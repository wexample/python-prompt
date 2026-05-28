from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.example.abstract_response_example import (
        AbstractResponseExample,
    )


@base_class
class CodePromptResponse(AbstractPromptResponse):
    """Display a code snippet, optionally with a language label and line numbers.

    Unlike ``CommandPromptResponse`` (which is shell-only and prefixes lines
    with a prompt character), this response renders the code as-is. Compose
    with ``frame`` for a boxed snippet.
    """

    code: str | list[str] = public_field(
        description="Code snippet. A list is joined with newlines.",
    )
    language: str | None = public_field(
        default=None,
        description="Optional language tag (e.g. 'python', 'php', 'js') displayed as a header.",
    )
    line_numbers: bool = public_field(
        default=False,
        description="Prefix each line with its 1-based line number.",
    )

    @classmethod
    def create_code(
        cls,
        code: str | list[str],
        language: str | None = None,
        line_numbers: bool = False,
        verbosity: "VerbosityLevel | None" = None,
    ) -> CodePromptResponse:
        return cls(
            lines=[],
            code=code,
            language=language,
            line_numbers=line_numbers,
            verbosity=verbosity,
        )

    @classmethod
    def get_example_class(cls) -> type[AbstractResponseExample]:
        from wexample_prompt.example.response.code_example import CodeExample

        return CodeExample

    def render(self, context: "PromptContext | None" = None) -> str | None:
        from wexample_prompt.common.prompt_context import PromptContext
        from wexample_prompt.common.prompt_response_line import PromptResponseLine
        from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
        from wexample_prompt.enums.terminal_color import TerminalColor
        from wexample_prompt.enums.text_style import TextStyle

        context = PromptContext.create_if_none(context=context)

        if not self._verbosity_context_allows_display(context=context):
            return None

        code_str = (
            self.code if isinstance(self.code, str) else "\n".join(self.code)
        )

        lines: list[PromptResponseLine] = []

        if self.language:
            lines.append(
                PromptResponseLine(
                    segments=[
                        PromptResponseSegment(
                            text=f"{self.language}",
                            color=TerminalColor.LIGHT_BLACK,
                            styles=[TextStyle.DIM],
                        ),
                    ]
                )
            )

        code_lines = code_str.split("\n")
        width = len(str(len(code_lines))) if self.line_numbers else 0

        for idx, line in enumerate(code_lines, start=1):
            segments: list[PromptResponseSegment] = []
            if self.line_numbers:
                segments.append(
                    PromptResponseSegment(
                        text=f"{idx:>{width}} │ ",
                        color=TerminalColor.LIGHT_BLACK,
                    )
                )
            segments.append(PromptResponseSegment(text=line))
            lines.append(PromptResponseLine(segments=segments))

        self.lines = lines
        return super().render(context=context)
