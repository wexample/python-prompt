from typing import TYPE_CHECKING, Optional

from wexample_helpers.const.types import Kwargs
from wexample_prompt.common.prompt_context import PromptContext

if TYPE_CHECKING:
    from wexample_prompt.enums.terminal_color import TerminalColor
    from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
    from wexample_prompt.common.io_manager import IoManager


class SubtitlePromptResponseManagerMixin:
    def subtitle(
            self: "IoManager",
            message: str,
            color: Optional["TerminalColor"] = None,
            character: Optional[str] = None,
            width: Optional[int] = None,
            context: Optional[PromptContext] = None,
            **kwargs: Kwargs
    ) -> "AbstractPromptResponse":
        from wexample_prompt.responses.titles.subtitle_prompt_response import SubtitlePromptResponse

        response = SubtitlePromptResponse.create_subtitle(
            text=message,
            color=color,
            character=character,
            width=width,
        )

        return self.print_response(
            response=response,
            context=SubtitlePromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs
            )
        )
