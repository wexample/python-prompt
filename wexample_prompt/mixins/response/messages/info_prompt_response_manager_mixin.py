from typing import TYPE_CHECKING, Optional

from wexample_helpers.const.types import Kwargs

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.responses.messages.info_prompt_response import InfoPromptResponse
    from wexample_prompt.common.io_manager import IoManager


class InfoPromptResponseManagerMixin:
    def info(
            self: "IoManager",
            message: str,
            context: Optional["PromptContext"] = None,
            **kwargs: Kwargs
    ) -> "InfoPromptResponse":
        from wexample_prompt.responses.messages.info_prompt_response import InfoPromptResponse

        response = InfoPromptResponse.create_info(
            message=message,
        )

        return self.print_response(
            response=response,
            context=InfoPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs
            )
        )
