"""Mixin for handling interactive choice prompts in IoManager."""
from typing import TYPE_CHECKING, Optional, List, Any, Union, Mapping

from wexample_helpers.const.types import Kwargs
from wexample_prompt.common.prompt_context import PromptContext

if TYPE_CHECKING:
    from wexample_prompt.responses.interactive.choice_prompt_response import ChoicePromptResponse
    from wexample_prompt.common.io_manager import IoManager


class ChoicePromptResponseManagerMixin:
    def choice(
            self: "IoManager",
            question: str,
            choices: Union[List[Any], Mapping[Any, Any]],
            default: Optional[Any] = None,
            abort: Optional[bool | str]  = None,
            context: Optional[PromptContext] = None,
            reset_on_finish: bool = False,
            answer: Any = None,
            **kwargs: Kwargs,
    ) -> "ChoicePromptResponse":
        from wexample_prompt.responses.interactive.choice_prompt_response import ChoicePromptResponse

        response = ChoicePromptResponse.create_choice(
            question=question,
            choices=choices,
            default=default,
            abort=abort,
            reset_on_finish=reset_on_finish,
        )

        response.ask(
            context=ChoicePromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
            answer=answer
        )

        return response
