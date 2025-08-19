from typing import TYPE_CHECKING, Optional, Any, List

from wexample_prompt.output.abstract_output_handler import AbstractOutputHandler

if TYPE_CHECKING:
    from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
    from wexample_prompt.common.prompt_context import PromptContext


class BufferOutputHandler(AbstractOutputHandler):
    """Output handler that buffers responses instead of writing to stdout.

    - Stores the original response objects in `buffer` (preserving legacy behavior).
    - Returns the rendered string (aligned with current handlers like StdoutOutputHandler).
    """

    _buffer: List["AbstractPromptResponse"] = []

    @property
    def buffer(self) -> List["AbstractPromptResponse"]:
        return self._buffer

    def print(self, response: "AbstractPromptResponse", context: Optional["PromptContext"] = None) -> Any:
        # Preserve legacy: store the response object
        self._buffer.append(response)

        # Align with new API: return the rendered output
        return response.render(context=context)
