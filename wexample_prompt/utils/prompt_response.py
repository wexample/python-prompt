import os
from typing import Optional, List, Dict

from pydantic import BaseModel

from wexample_prompt.const.types import LineDict
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.utils.prompt_response_line import PromptResponseLine


class PromptResponse(BaseModel):
    lines: List[PromptResponseLine] = []
    message_type: MessageType

    def __init__(self, message: Optional[str] = None, message_type: MessageType = MessageType.LOG) -> None:
        super().__init__(message=message, message_type=message_type)

        if message:
            self.lines = self.split_lines(message)

    @staticmethod
    def split_lines(message: str) -> List[PromptResponseLine]:
        lines = message.split(os.linesep)
        return [PromptResponseLine(message=message) for message in lines]

    @staticmethod
    def from_lines(messages: List[str]) -> 'PromptResponse':
        response = PromptResponse()

        for message in messages:
            response.lines.append(PromptResponseLine.from_message(message=message))

        return response

    @staticmethod
    def from_multiline_message(message: str) -> 'PromptResponse':
        response = PromptResponse()
        response.lines = response.split_lines(message)

        return response

    @staticmethod
    def from_dicts(lines: List[LineDict]) -> 'PromptResponse':
        response = PromptResponse()

        for line_dict in lines:
            response.lines.append(PromptResponseLine.from_dict(line_dict))

        return response
