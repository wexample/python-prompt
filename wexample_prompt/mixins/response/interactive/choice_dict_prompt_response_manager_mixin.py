"""Mixin for managing choice dict prompt responses."""
from typing import Dict, Optional, TYPE_CHECKING

from wexample_helpers.const.types import Kwargs
from wexample_prompt.common.prompt_context import PromptContext

if TYPE_CHECKING:
    from wexample_prompt.responses.interactive.choice_dict_prompt_response import ChoiceDictPromptResponse
    from wexample_prompt.common.io_manager import IoManager


class ChoiceDictPromptResponseManagerMixin:
    """Mixin class for managing choice dict prompt responses."""

    def choice_dict(
            self: "IoManager",
            question: str,
            choices: Dict[str, str],
            default: Optional[str] = None,
            abort: Optional[str] = "> Abort",
            context: Optional[PromptContext] = None,
            **kwargs: Kwargs,
    ) -> "ChoiceDictPromptResponse":
        from wexample_prompt.responses.interactive.choice_dict_prompt_response import ChoiceDictPromptResponse

        response = ChoiceDictPromptResponse.create_choice_dict(
            question=question,
            choices=choices,
            default=default,
            abort=abort,
        )

        self.print_response(
            response=response,
            context=ChoiceDictPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            )
        )

        return response
