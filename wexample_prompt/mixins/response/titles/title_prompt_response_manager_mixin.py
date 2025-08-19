from typing import TYPE_CHECKING, Optional, cast, Any

from wexample_helpers.const.types import Kwargs
from wexample_prompt.common.prompt_context import PromptContext

if TYPE_CHECKING:
    from wexample_prompt.enums.terminal_color import TerminalColor
    from wexample_prompt.common.io_manager import IoManager


class TitlePromptResponseManagerMixin:
    def title(
            self: "IoManager",
            message: str,
            color: Optional["TerminalColor"] = None,
            character: Optional[str] = None,
            width: Optional[int] = None,
            context: Optional[PromptContext] = None,
            **kwargs: Kwargs
    ) -> Any:
        from wexample_prompt.responses.titles.title_prompt_response import TitlePromptResponse

        response = TitlePromptResponse.create_title(
            text=message,
            color=color,
            character=character,
            width=width,
        )

        return cast("IoManager", self).print_response(
            response=response,
            context=TitlePromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs
            )
        )
