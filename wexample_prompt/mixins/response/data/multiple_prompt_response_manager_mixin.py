"""Mixin for managing multiple prompt responses."""
from typing import List, TYPE_CHECKING

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.responses.data.multiple_prompt_response import MultiplePromptResponse

if TYPE_CHECKING:
    from wexample_prompt.common.io_manager import IoManager


class MultiplePromptResponseManagerMixin:
    """Mixin for managing multiple prompt responses in IoManager."""

    def multiple(
        self: "IoManager",
        responses: List[AbstractPromptResponse],
        **kwargs,
    ) -> MultiplePromptResponse:
        """Create a multiple prompt response."""
        return MultiplePromptResponse.create_multiple(
            responses=responses,
            **kwargs,
        )
