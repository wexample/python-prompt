from typing import TYPE_CHECKING, Optional

from wexample_prompt.common.prompt_context import PromptContext

if TYPE_CHECKING:
    from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse


class LogPromptResponseManagerMixin:
    def log(self, message: str, context: Optional[PromptContext] = None) -> "AbstractPromptResponse":
        from wexample_prompt.responses.messages.log_prompt_response import LogPromptResponse

        response = LogPromptResponse.create_log(
            message=message,
        )

        self.print_response(
            response=response,
            context=context
        )
        
        return response
