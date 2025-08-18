from typing import TYPE_CHECKING, Optional

from wexample_helpers.const.types import Kwargs
from wexample_prompt.common.prompt_context import PromptContext

if TYPE_CHECKING:
    from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse


class TitlePromptResponseManagerMixin:
    def title(
            self,
            message: str,
            color: Optional["TerminalColor"] = None,
            context: Optional[PromptContext] = None,
            **kwargs: Kwargs
    ) -> "AbstractPromptResponse":
        from wexample_prompt.responses.titles.title_prompt_response import TitlePromptResponse

        response = TitlePromptResponse.create_title(
            text=message,
        )

        self.print_response(
            response=response,
            context=TitlePromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs
            )
        )

        return response
