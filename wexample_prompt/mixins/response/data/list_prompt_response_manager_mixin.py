from typing import TYPE_CHECKING, Any, List, Optional

from wexample_helpers.const.types import Kwargs
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.verbosity_level import VerbosityLevel

if TYPE_CHECKING:
    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.enums.terminal_color import TerminalColor
    from wexample_prompt.responses.data.list_prompt_response import ListPromptResponse


class ListPromptResponseManagerMixin:
    def list(
        self: "IoManager",
        items: List[str],
        bullet: str = "•",
        color: Optional["TerminalColor"] = None,
        verbosity: Optional[VerbosityLevel] = VerbosityLevel.DEFAULT,
        context: Optional[PromptContext] = None,
        **kwargs: Kwargs
    ) -> "ListPromptResponse":
        from wexample_prompt.responses.data.list_prompt_response import (
            ListPromptResponse,
        )

        response = ListPromptResponse.create_list(
            items=items,
            bullet=bullet,
            color=color,
            verbosity=verbosity,
        )

        return self.print_response(
            response=response,
            context=ListPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
        )
