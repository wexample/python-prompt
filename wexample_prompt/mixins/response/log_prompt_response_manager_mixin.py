from typing import TYPE_CHECKING, Optional

from wexample_helpers.const.types import Kwargs
from wexample_prompt.common.prompt_context import PromptContext

if TYPE_CHECKING:
    from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse


class LogPromptResponseManagerMixin:
    def log(
            self,
            message: str,
            context: Optional[PromptContext] = None,
            **kwargs:Kwargs
    ) -> "AbstractPromptResponse":
        from wexample_prompt.responses.log_prompt_response import LogPromptResponse

        response = LogPromptResponse.create_log(
            message=message,
        )

        self.print_response(
            response=response,
            context=LogPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs
            )
        )

        return response
