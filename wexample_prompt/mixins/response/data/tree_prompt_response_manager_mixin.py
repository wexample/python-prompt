"""Mixin for handling tree responses in IoManager."""
from typing import Dict, Any, Optional, TYPE_CHECKING

from wexample_helpers.const.types import Kwargs
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.verbosity_level import VerbosityLevel

if TYPE_CHECKING:
    from wexample_prompt.responses.data.tree_prompt_response import TreePromptResponse
    from wexample_prompt.common.io_manager import IoManager


class TreePromptResponseManagerMixin:
    """Mixin for IoManager to handle tree responses."""

    def tree(
            self: "IoManager",
            data: Dict[str, Any],
            verbosity: Optional[VerbosityLevel] = VerbosityLevel.DEFAULT,
            context: Optional[PromptContext] = None,
            **kwargs: Kwargs,
    ) -> "TreePromptResponse":
        from wexample_prompt.responses.data.tree_prompt_response import TreePromptResponse

        response = TreePromptResponse.create_tree(
            data=data,
            verbosity=verbosity,
        )

        return self.print_response(
            response=response,
            context=TreePromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
        )
