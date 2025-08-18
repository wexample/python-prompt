"""Mixin for handling table responses in IoManager."""
from typing import List, Optional, Any, TYPE_CHECKING

from wexample_helpers.const.types import Kwargs
from wexample_prompt.common.prompt_context import PromptContext

if TYPE_CHECKING:
    from wexample_prompt.responses.data.table_prompt_response import TablePromptResponse
    from wexample_prompt.common.io_manager import IoManager


class TablePromptResponseManagerMixin:
    """Mixin for IoManager to handle table responses."""

    def table(
            self: "IoManager",
            data: List[List[Any]],
            headers: Optional[List[str]] = None,
            title: Optional[str] = None,
            context: Optional[PromptContext] = None,
            **kwargs: Kwargs,
    ) -> "TablePromptResponse":
        from wexample_prompt.responses.data.table_prompt_response import TablePromptResponse

        response = TablePromptResponse.create_table(
            data=data,
            headers=headers,
            title=title,
        )

        self.print_response(
            response=response,
            context=TablePromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
        )

        return response
