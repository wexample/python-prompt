"""Base class for prompt responses."""
from typing import List, Dict, Any, TextIO, Type, Optional, TYPE_CHECKING

from pydantic import Field

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.enums.response_type import ResponseType

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.example.abstract_response_example import AbstractResponseExample
    from wexample_prompt.common.prompt_response_line import PromptResponseLine


class BasePromptResponse(AbstractPromptResponse):
    """Base class for all prompt responses."""

    @classmethod
    def get_example_class(cls) -> Type["AbstractResponseExample"]:
        """Get the example class for this response type.

        Returns:
            Type: The example class
        """
        from wexample_prompt.example.response.messages.base_example import BaseExample
        return BaseExample

    @classmethod
    def create_base(
        cls,
        lines: List["PromptResponseLine"],
        context: Optional["PromptContext"] = None,
        response_type: ResponseType = ResponseType.PLAIN,
        message_type: MessageType = MessageType.LOG,
        metadata: Dict[str, Any] = None,
        **kwargs
    ) -> "BasePromptResponse":
        """Create a base prompt response.

        Args:
            lines: List of response lines
            context: Optional prompt context
            response_type: Response type
            message_type: Message type
            metadata: Optional metadata
            **kwargs: Additional keyword arguments

        Returns:
            BasePromptResponse: A new base prompt response
        """
        return cls(
            lines=lines,
            context=context,
            response_type=response_type,
            message_type=message_type,
            metadata=metadata or {}
        )

    def print(
        self,
        output: TextIO = None,
        end: str = "\n",
        flush: bool = True,
    ) -> None:
        """Print the response.

        Args:
            output: Output stream
            end: End string
            flush: Whether to flush the output
        """
        rendered = self.render()
        if rendered:
            print(rendered, file=output, end=end, flush=flush)

        # Exit if fatal
        if self.context and self.context.fatal:
            self._on_fatal()

    def _on_fatal(self):
        """Handle fatal errors."""
        import sys
        sys.exit(self.context.exit_code)

    def append(self, other: "BasePromptResponse") -> "BasePromptResponse":
        """Combine this response with another.

        Args:
            other: Other response to append

        Returns:
            BasePromptResponse: Combined response
        """
        return self.__class__.create_base(
            lines=self.lines + other.lines,
            context=self.context,
            response_type=self.response_type,
            message_type=self.message_type,
            metadata={**self.metadata, **other.metadata}
        )
