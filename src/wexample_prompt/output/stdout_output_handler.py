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
            print(rendered_response, file=sys.stdout, end="\n")

        return rendered_response

    def erase(
            self,
            response: AbstractPromptResponse,
    ) -> Any:
        print(response.render_erase())
