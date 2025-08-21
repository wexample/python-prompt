"""Mixin for handling interactive choice prompts in IoManager."""

from typing import TYPE_CHECKING, Any, List, Optional, Union
from collections.abc import Mapping

from wexample_helpers.const.types import Kwargs
from wexample_prompt.const.types import LineMessage
from wexample_prompt.enums.verbosity_level import VerbosityLevel

if TYPE_CHECKING:
    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.responses.interactive.choice_prompt_response import (
        ChoicePromptResponse,
    )


class ChoicePromptResponseManagerMixin:
    def choice(
        self: "IoManager",
        question: LineMessage,
        choices: list[Any] | Mapping[Any, Any],
        default: Any | None = None,
        abort: bool | str | None = None,
        verbosity: VerbosityLevel | None = VerbosityLevel.DEFAULT,
        context: Optional["PromptContext"] = None,
        reset_on_finish: bool = False,
        predefined_answer: Any = None,
        **kwargs: Kwargs,
    ) -> "ChoicePromptResponse":
        from wexample_prompt.responses.interactive.choice_prompt_response import (
            ChoicePromptResponse,
        )

        response = ChoicePromptResponse.create_choice(
            question=question,
            choices=choices,
            default=default,
            abort=abort,
            verbosity=verbosity,
            reset_on_finish=reset_on_finish,
            predefined_answer=predefined_answer,
        )

        return self.print_response(
            response=response,
            context=ChoicePromptResponse.rebuild_context_for_kwargs(
                context=context, parent_kwargs=kwargs
            ),
        )
