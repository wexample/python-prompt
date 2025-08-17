import sys
from typing import TYPE_CHECKING

from wexample_prompt.output.abstract_output_handler import AbstractOutputHandler

if TYPE_CHECKING:
    from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse


class StdoutOutputHandler(AbstractOutputHandler):
    def print(self, response: "AbstractPromptResponse") -> None:
        print(response.render(), file=sys.stdout, end="\n")
