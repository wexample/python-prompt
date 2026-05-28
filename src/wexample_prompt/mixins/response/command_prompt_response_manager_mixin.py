from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_helpers.const.types import Kwargs

    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.responses.command_prompt_response import (
        CommandPromptResponse,
    )


class CommandPromptResponseManagerMixin:
    def command(
        self: IoManager,
        command: str | list[str],
        output: str | list[str] | None = None,
        prompt_char: str = "$",
        executed: bool = False,
        verbosity: VerbosityLevel | None = None,
        context: PromptContext | None = None,
        **kwargs: Kwargs,
    ) -> CommandPromptResponse:
        from wexample_prompt.responses.command_prompt_response import (
            CommandPromptResponse,
        )

        response = CommandPromptResponse.create_command(
            command=command,
            output=output,
            prompt_char=prompt_char,
            executed=executed,
            verbosity=(
                verbosity if verbosity is not None else self.default_response_verbosity
            ),
        )

        return self.print_response(
            response=response,
            context=CommandPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
        )
