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
            choices: Optional[Dict[str, str]] = None,
            preset: Optional[str] = None,
            default: Optional[str] = None,
            abort: Optional[bool | str]  = None,
            context: Optional[PromptContext] = None,
            **kwargs: Any,
    ) -> "ConfirmPromptResponse":
        from wexample_prompt.responses.interactive.confirm_prompt_response import ConfirmPromptResponse

        response = ConfirmPromptResponse.create_confirm(
            question=question,
            choices=choices,
            preset=preset,
            default=default,
            abort=abort,
            **kwargs,
        )

        return self.print_response(
            response=response,
            context=ConfirmPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
        )
