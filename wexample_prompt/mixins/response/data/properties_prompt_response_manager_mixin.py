"""Properties response manager mixin."""

from typing import TYPE_CHECKING, Any, Dict, Optional

from wexample_helpers.const.types import Kwargs

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.verbosity_level import VerbosityLevel

if TYPE_CHECKING:
    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.responses.data.properties_prompt_response import \
        PropertiesPromptResponse


class PropertiesPromptResponseManagerMixin:
    """Mixin for IoManager to handle properties responses."""

    def properties(
        self: "IoManager",
        properties: Dict[str, Any],
        title: Optional[str] = None,
        nested_indent: int = 2,
        verbosity: Optional[VerbosityLevel] = VerbosityLevel.DEFAULT,
        context: Optional[PromptContext] = None,
        **kwargs: Kwargs,
    ) -> "PropertiesPromptResponse":
        from wexample_prompt.responses.data.properties_prompt_response import \
            PropertiesPromptResponse

        response = PropertiesPromptResponse.create_properties(
            properties=properties,
            title=title,
            nested_indent=nested_indent,
            verbosity=verbosity,
        )

        return self.print_response(
            response=response,
            context=PropertiesPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
        )
