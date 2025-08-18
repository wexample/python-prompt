from typing import TYPE_CHECKING, Optional

from wexample_helpers.const.types import Kwargs
from wexample_prompt.common.prompt_context import PromptContext

if TYPE_CHECKING:
    from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse


class EchoPromptResponseManagerMixin:
    def echo(
            self,
            message: str,
            context: Optional[PromptContext] = None,
            **kwargs:Kwargs
    ) -> "AbstractPromptResponse":
        from wexample_prompt.responses.echo_prompt_response import EchoPromptResponse

        response = EchoPromptResponse.create_echo(
            message=message,
        )

        self.print_response(
            response=response,
            context=EchoPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs
            )
        )

        return response
