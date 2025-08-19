"""Mixin for managing confirmation dialogs."""
from typing import Any, Dict, Optional, TYPE_CHECKING

from wexample_prompt.common.prompt_context import PromptContext

if TYPE_CHECKING:
    from wexample_prompt.responses.interactive.confirm_prompt_response import ConfirmPromptResponse
    from wexample_prompt.common.io_manager import IoManager


class ConfirmPromptResponseManagerMixin:
    """Mixin class for managing confirmation dialog prompt responses."""

    def confirm(
            self: "IoManager",
            question: str = "Please confirm:",
            choices: Optional[Dict[str, tuple]] = None,
            default: Optional[str] = None,
            width: Optional[int] = None,
            reset_on_finish: bool = False,
            context: Optional[PromptContext] = None,
            answer: Any = None,
            **kwargs: Any,
    ) -> "ConfirmPromptResponse":
        from wexample_prompt.responses.interactive.confirm_prompt_response import ConfirmPromptResponse

        response = ConfirmPromptResponse.create_confirm(
            question=question,
            choices=choices,
            default=default,
            width=width,
            reset_on_finish=reset_on_finish,
        )

        response.ask(
            context=ConfirmPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
            answer=answer
        )

        return response
