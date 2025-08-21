from typing import TYPE_CHECKING, Optional, cast

from wexample_helpers.const.types import Kwargs

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.const.types import LineMessage
from wexample_prompt.enums.verbosity_level import VerbosityLevel

if TYPE_CHECKING:
    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.enums.terminal_color import TerminalColor
    from wexample_prompt.responses.abstract_prompt_response import (
        AbstractPromptResponse,
    )


class TitlePromptResponseManagerMixin:
    def title(
        self: "IoManager",
        text: LineMessage,
        color: Optional["TerminalColor"] = None,
        character: Optional[str] = None,
        width: Optional[int] = None,
        verbosity: Optional[VerbosityLevel] = VerbosityLevel.DEFAULT,
        context: Optional[PromptContext] = None,
        **kwargs: Kwargs
    ) -> "AbstractPromptResponse":
        from wexample_prompt.responses.titles.title_prompt_response import (
            TitlePromptResponse,
        )

        response = TitlePromptResponse.create_title(
            text=text,
            color=color,
            character=character,
            width=width,
            verbosity=verbosity,
        )

        return cast("IoManager", self).print_response(
            response=response,
            context=TitlePromptResponse.rebuild_context_for_kwargs(
                context=context, parent_kwargs=kwargs
            ),
        )
