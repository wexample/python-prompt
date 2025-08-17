from typing import List

from pydantic import Field

from wexample_prompt.output.abstract_output_handler import AbstractOutputHandler
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse


class BufferOutputHandler(AbstractOutputHandler):
    buffer: List[AbstractPromptResponse] = Field(default_factory=list)

    def print(self, response: AbstractPromptResponse) -> None:
        self.buffer.append(response)
