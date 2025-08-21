from typing import TYPE_CHECKING, Optional

from wexample_helpers.const.types import Kwargs
from wexample_prompt.const.types import LineMessage
from wexample_prompt.enums.verbosity_level import VerbosityLevel

if TYPE_CHECKING:
    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.responses.messages.info_prompt_response import \
        InfoPromptResponse


class InfoPromptResponseManagerMixin:
    def info(
        self: "IoManager",
        message: LineMessage,
        verbosity: Optional[VerbosityLevel] = VerbosityLevel.DEFAULT,
        context: Optional["PromptContext"] = None,
        **kwargs: Kwargs
    ) -> "InfoPromptResponse":
        from wexample_prompt.responses.messages.info_prompt_response import \
            InfoPromptResponse

        response = InfoPromptResponse.create_info(
            message=message,
            verbosity=verbosity,
        )

        return self.print_response(
            response=response,
            context=InfoPromptResponse.rebuild_context_for_kwargs(
                context=context, parent_kwargs=kwargs
            ),
        )
