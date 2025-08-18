"""Properties response manager mixin."""
from typing import Dict, Any, Optional, TYPE_CHECKING

from wexample_helpers.const.types import Kwargs
from wexample_prompt.common.prompt_context import PromptContext

if TYPE_CHECKING:
    from wexample_prompt.responses.data.properties_prompt_response import PropertiesPromptResponse


class PropertiesPromptResponseManagerMixin:
    """Mixin for IoManager to handle properties responses."""

    def properties(
        self,
        properties: Dict[str, Any],
        title: Optional[str] = None,
        nested_indent: int = 2,
        context: Optional[PromptContext] = None,
        **kwargs: Kwargs,
    ) -> "PropertiesPromptResponse":
        from wexample_prompt.responses.data.properties_prompt_response import PropertiesPromptResponse

        response = PropertiesPromptResponse.create_properties(
            properties=properties,
            title=title,
            nested_indent=nested_indent,
        )

        self.print_response(
            response=response,
            context=PropertiesPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
        )

        return response
