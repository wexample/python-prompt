from typing import TYPE_CHECKING, List, Optional

from wexample_helpers.const.types import Kwargs
from wexample_prompt.common.prompt_context import PromptContext

if TYPE_CHECKING:
    from wexample_prompt.enums.terminal_color import TerminalColor
    from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
    from wexample_prompt.common.io_manager import IoManager


class ListPromptResponseManagerMixin:
    def list(
            self: "IoManager",
            items: List[str],
            bullet: str = "•",
            color: Optional["TerminalColor"] = None,
            context: Optional[PromptContext] = None,
            **kwargs: Kwargs) -> "AbstractPromptResponse":
        from wexample_prompt.responses.data.list_prompt_response import ListPromptResponse

        response = ListPromptResponse.create_list(
            items=items,
            bullet=bullet,
            color=color,
        )

        self.print_response(
            response=response,
            context=ListPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
        )

        return response
