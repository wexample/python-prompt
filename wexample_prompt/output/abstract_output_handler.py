from typing import TYPE_CHECKING

from wexample_helpers.classes.extended_base_model import ExtendedBaseModel

if TYPE_CHECKING:
    from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse


class AbstractOutputHandler(ExtendedBaseModel):
    def print(self, response: "AbstractPromptResponse") -> None:
        ...
