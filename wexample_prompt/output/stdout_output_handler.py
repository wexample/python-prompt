import sys
from typing import TYPE_CHECKING, Optional, Any

from wexample_prompt.output.abstract_output_handler import AbstractOutputHandler

if TYPE_CHECKING:
    from wexample_prompt.responses.abstract_prompt_response import (
        AbstractPromptResponse,
    )
    from wexample_prompt.common.prompt_context import PromptContext


class StdoutOutputHandler(AbstractOutputHandler):
    def print(
        self,
        response: "AbstractPromptResponse",
        context: Optional["PromptContext"] = None,
    ) -> Any:
        rendered_response = response.render(context=context)
        if rendered_response:
            print(rendered_response, file=sys.stdout, end="\n")

        return rendered_response
