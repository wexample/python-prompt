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
class CommandPromptResponse(AbstractPromptResponse):
    """Display a shell-like command, optionally with its output.

    Used to surface a command line in transcripts and reports — either as
    something to run (``executed=False``, default) or as something that was
    already run (``executed=True``, replaces the prompt char with a green
    checkmark).
    """

    command: str | list[str] = public_field(
        description="Shell command to display. Accepts a pre-joined string or a list of argv tokens (joined via shlex).",
    )
    executed: bool = public_field(
        default=False,
        description="When True, render with a green ✓ instead of the prompt char",
    )
    output: str | list[str] | None = public_field(
        default=None,
        description="Optional command output, rendered indented below the command",
    )
    prompt_char: str = public_field(
        default="$",
        description="Prefix character before the command (e.g. '$', '>', '#', '>>>')",
    )

    @classmethod
    def create_command(
        cls,
        command: str | list[str],
        output: str | list[str] | None = None,
        prompt_char: str = "$",
        executed: bool = False,
        verbosity: "VerbosityLevel | None" = None,
    ) -> CommandPromptResponse:
        return cls(
            lines=[],
            command=command,
            output=output,
            prompt_char=prompt_char,
            executed=executed,
            verbosity=verbosity,
        )

    def _resolve_command_string(self) -> str:
        if isinstance(self.command, str):
            return self.command
        import shlex

        return shlex.join(self.command)

    @classmethod
    def get_example_class(cls) -> type[AbstractResponseExample]:
        from wexample_prompt.example.response.command_example import CommandExample

        return CommandExample

    def render(self, context: "PromptContext | None" = None) -> str | None:
        from wexample_prompt.common.prompt_context import PromptContext
        from wexample_prompt.common.prompt_response_line import PromptResponseLine
        from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
        from wexample_prompt.enums.terminal_color import TerminalColor
        from wexample_prompt.enums.text_style import TextStyle

        context = PromptContext.create_if_none(context=context)

        if not self._verbosity_context_allows_display(context=context):
            return None

        command_str = self._resolve_command_string()
        if not command_str:
            self.lines = []
            return super().render(context=context)

        if self.executed:
            prefix_seg = PromptResponseSegment(
                text="✓ ",
                color=TerminalColor.GREEN,
                styles=[TextStyle.BOLD],
            )
        else:
            prefix_seg = PromptResponseSegment(
                text=f"{self.prompt_char} ",
                color=TerminalColor.LIGHT_BLACK,
            )

        lines: list[PromptResponseLine] = []

        # The command itself: parse markup, color the un-styled parts in cyan,
        # and prepend the prefix segment to the very first line only.
        cmd_lines = PromptResponseLine.create_from_string(
            text=command_str, color=TerminalColor.CYAN
        )
        if cmd_lines:
            first = cmd_lines[0]
            first.segments = [prefix_seg] + first.segments
            lines.extend(cmd_lines)

        # Output: indent 2 spaces, render dim/gray. Empty output is skipped.
        if self.output is not None:
            raw = [self.output] if isinstance(self.output, str) else list(self.output)
            for chunk in raw:
                for sub in chunk.split("\n"):
                    out_lines = PromptResponseLine.create_from_string(
                        text=f"  {sub}", color=TerminalColor.LIGHT_BLACK
                    )
                    lines.extend(out_lines)

        self.lines = lines
        return super().render(context=context)
