"""Properties response manager mixin."""
from typing import Dict, Any, Optional, TYPE_CHECKING, Any as _Any

from wexample_helpers.const.types import Kwargs
from wexample_prompt.common.prompt_context import PromptContext

if TYPE_CHECKING:
    from wexample_prompt.responses.data.properties_prompt_response import PropertiesPromptResponse
    from wexample_prompt.common.io_manager import IoManager


class PropertiesPromptResponseManagerMixin:
    """Mixin for IoManager to handle properties responses."""

    def properties(
            self: "IoManager",
            properties: Dict[str, Any],
            title: Optional[str] = None,
            nested_indent: int = 2,
            context: Optional[PromptContext] = None,
            **kwargs: Kwargs,
    ) -> _Any:
        from wexample_prompt.responses.data.properties_prompt_response import PropertiesPromptResponse

        response = PropertiesPromptResponse.create_properties(
            properties=properties,
            title=title,
            nested_indent=nested_indent,
        )

        return self.print_response(
            response=response,
            context=PropertiesPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
        )
