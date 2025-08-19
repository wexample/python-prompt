from typing import TYPE_CHECKING, Optional, Any

from wexample_helpers.const.types import Kwargs

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.common.io_manager import IoManager


class DebugPromptResponseManagerMixin:
    def debug(
            self: "IoManager",
            message: str,
            context: Optional["PromptContext"] = None,
            **kwargs: Kwargs
    ) -> Any:
        from wexample_prompt.responses.messages.debug_prompt_response import DebugPromptResponse

        response = DebugPromptResponse.create_debug(
            message=message,
        )

        return self.print_response(
            response=response,
            context=DebugPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs
            )
        )
