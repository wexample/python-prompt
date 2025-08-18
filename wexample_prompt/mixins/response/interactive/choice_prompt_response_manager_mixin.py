"""Mixin for handling interactive choice prompts in IoManager."""
from typing import TYPE_CHECKING, Optional, List, Any

from InquirerPy.utils import InquirerPyDefault
from wexample_helpers.const.types import Kwargs
from wexample_prompt.common.prompt_context import PromptContext

if TYPE_CHECKING:
    from wexample_prompt.responses.interactive.choice_prompt_response import ChoicePromptResponse


class ChoicePromptResponseManagerMixin:
    def choice(
        self,
        question: str,
        choices: List[Any],
        default: Optional[InquirerPyDefault] = None,
        abort: Optional[str] = "> Abort",
        context: Optional[PromptContext] = None,
        **kwargs: Kwargs,
    ) -> "ChoicePromptResponse":
        from wexample_prompt.responses.interactive.choice_prompt_response import ChoicePromptResponse

        response = ChoicePromptResponse.create_choice(
            question=question,
            choices=choices,
            default=default,
            abort=abort,
        )

        self.print_response(
            response=response,
            context=ChoicePromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
        )

        return response
