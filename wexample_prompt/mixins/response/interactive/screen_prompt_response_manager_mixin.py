"""Mixin for handling interactive screen response in IoManager."""
from typing import TYPE_CHECKING, Optional, Callable, Any

from wexample_helpers.const.types import Kwargs
from wexample_prompt.common.prompt_context import PromptContext

if TYPE_CHECKING:
    from wexample_prompt.responses.interactive.screen_prompt_response import ScreenPromptResponse
    from wexample_prompt.common.io_manager import IoManager


class ScreenPromptResponseManagerMixin:
    def screen(
            self: "IoManager",
            *,
            callback: Callable[["ScreenPromptResponse"], Any],
            height: int = 30,
            reset_on_finish: bool = False,
            context: Optional[PromptContext] = None,
            **kwargs: Kwargs,
    ) -> "ScreenPromptResponse":
        from wexample_prompt.responses.interactive.screen_prompt_response import ScreenPromptResponse

        response = ScreenPromptResponse.create_screen(
            callback=callback,
            height=height,
            reset_on_finish=reset_on_finish,
        )

        return self.print_response(
            response=response,
            context=ScreenPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
        )
