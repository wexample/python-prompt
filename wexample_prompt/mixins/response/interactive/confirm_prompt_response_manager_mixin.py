"""Mixin for managing confirmation dialogs."""

from typing import Any, Dict, Optional, TYPE_CHECKING

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.const.types import LineMessage

if TYPE_CHECKING:
    from wexample_prompt.responses.interactive.confirm_prompt_response import (
        ConfirmPromptResponse,
    )
    from wexample_prompt.common.io_manager import IoManager


class ConfirmPromptResponseManagerMixin:
    """Mixin class for managing confirmation dialog prompt responses."""

    def confirm(
        self: "IoManager",
        question: LineMessage = "Please confirm:",
        choices: Optional[Dict[str, tuple]] = None,
        default: Optional[str] = None,
        width: Optional[int] = None,
        verbosity: Optional[VerbosityLevel] = VerbosityLevel.DEFAULT,
        reset_on_finish: bool = False,
        context: Optional[PromptContext] = None,
        predefined_answer: Any = None,
        **kwargs: Any,
    ) -> "ConfirmPromptResponse":
        from wexample_prompt.responses.interactive.confirm_prompt_response import (
            ConfirmPromptResponse,
        )

        response = ConfirmPromptResponse.create_confirm(
            question=question,
            choices=choices,
            default=default,
            width=width,
            verbosity=verbosity,
            reset_on_finish=reset_on_finish,
            predefined_answer=predefined_answer,
        )

        return self.print_response(
            response=response,
            context=ConfirmPromptResponse.rebuild_context_for_kwargs(
                context=context, parent_kwargs=kwargs
            ),
        )
