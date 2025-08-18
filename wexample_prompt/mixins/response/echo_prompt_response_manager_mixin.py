"""Mixin for base prompt response."""
from typing import TYPE_CHECKING, Optional

from wexample_prompt.common.prompt_context import PromptContext

if TYPE_CHECKING:
    from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse


class EchoPromptResponseManagerMixin:
    """Mixin for base prompt response."""

    def echo(
            self,
            message: str,
            context: Optional[PromptContext] = None
    ) -> "AbstractPromptResponse":
        """Create a base prompt response with no style"""

        from wexample_prompt.responses.echo_prompt_response import EchoPromptResponse

        response = EchoPromptResponse.create_echo(
            message=message,
        )

        self.print_response(
            response=response,
            context=context
        )

        return response
