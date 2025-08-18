"""Mixin for managing multiple prompt responses."""
from typing import List, TYPE_CHECKING, Optional

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse

if TYPE_CHECKING:
    from wexample_prompt.responses.data.multiple_prompt_response import MultiplePromptResponse
    from wexample_prompt.common.io_manager import IoManager


class MultiplePromptResponseManagerMixin:
    """Mixin for managing multiple prompt responses in IoManager."""

    def multiple(
            self: "IoManager",
            responses: List[AbstractPromptResponse],
            context: Optional[PromptContext] = None,
            **kwargs,
    ) -> "MultiplePromptResponse":
        """Create a multiple prompt response."""
        from wexample_prompt.responses.data.multiple_prompt_response import MultiplePromptResponse

        response = MultiplePromptResponse.create_multiple(
            responses=responses,
        )

        self.print_response(
            response=response,
            context=MultiplePromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
        )

        return response
