from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any

from wexample_prompt.output.abstract_output_handler import AbstractOutputHandler

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.responses.abstract_prompt_response import (
        AbstractPromptResponse,
    )


class StdoutOutputHandler(AbstractOutputHandler):
    def print(
            self,
            response: AbstractPromptResponse,
            context: PromptContext | None = None,
    ) -> Any:
        rendered_response = response.render(context=context)
        if rendered_response:
            # Equivalent of print
            # Use stdout directly for consistency with erase()
            sys.stdout.write(rendered_response + "\n")
            sys.stdout.flush()

        return rendered_response

    def erase(
            self,
            response: AbstractPromptResponse,
    ) -> Any:
        sys.stdout.write(self._render_erase(response))
        sys.stdout.flush()

    def _render_erase(self, response: AbstractPromptResponse) -> str:
        if not response.rendered_content:
            return ""
        lines = self._rendered_content.split("\n")
        parts = []
        # Move cursor up one line to reach the last printed line,
        # because printing typically ended with a trailing newline.
        parts.append("\x1b[F")
        for i in range(len(lines)):
            parts.append("\r\x1b[K")  # CR + Clear to end of line
            if i < len(lines) - 1:
                parts.append("\x1b[F")  # Cursor up one line

        parts.append("\r")
        return "".join(parts)
