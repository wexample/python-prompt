from typing import TYPE_CHECKING, Optional, Any

from wexample_helpers.const.types import Kwargs
from wexample_prompt.common.prompt_context import PromptContext

if TYPE_CHECKING:
    from wexample_prompt.common.io_manager import IoManager


class SeparatorPromptResponseManagerMixin:
    def separator(
            self: "IoManager",
            label: Optional[str] = None,
            width: Optional[int] = None,
            character: Optional[str] = None,
            context: Optional[PromptContext] = None,
            **kwargs: Kwargs
    ) -> Any:
        from wexample_prompt.responses.titles.separator_prompt_response import SeparatorPromptResponse

        response = SeparatorPromptResponse.create_separator(
            label=label,
            width=width,
            character=character or SeparatorPromptResponse.DEFAULT_CHARACTER,
        )

        return self.print_response(
            response=response,
            context=SeparatorPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs
            )
        )
