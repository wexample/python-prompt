from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_helpers.const.types import Kwargs

    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.responses.code_prompt_response import CodePromptResponse


class CodePromptResponseManagerMixin:
    def code(
        self: IoManager,
        code: str | list[str],
        language: str | None = None,
        line_numbers: bool = False,
        chevrons: bool = False,
        frame: str | bool | None = None,
        verbosity: VerbosityLevel | None = None,
        context: PromptContext | None = None,
        **kwargs: Kwargs,
    ) -> CodePromptResponse:
        from wexample_prompt.responses.code_prompt_response import CodePromptResponse

        response = CodePromptResponse.create_code(
            code=code,
            language=language,
            line_numbers=line_numbers,
            chevrons=chevrons,
            verbosity=(
                verbosity if verbosity is not None else self.default_response_verbosity
            ),
        )

        return self.print_response(
            response=response,
            context=CodePromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
            frame=frame,
        )
