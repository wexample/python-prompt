from typing import TYPE_CHECKING, Optional

from wexample_helpers.const.types import Kwargs
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.const.types import LineMessage

if TYPE_CHECKING:
    from wexample_prompt.responses.echo_prompt_response import EchoPromptResponse
    from wexample_prompt.common.io_manager import IoManager


class EchoPromptResponseManagerMixin:
    def echo(
            self: "IoManager",
            message: LineMessage,
            context: Optional[PromptContext] = None,
            **kwargs: Kwargs
    ) -> "EchoPromptResponse":
        from wexample_prompt.responses.echo_prompt_response import EchoPromptResponse

        response = EchoPromptResponse.create_echo(
            message=message,
        )

        return self.print_response(
            response=response,
            context=EchoPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs
            )
        )
