from typing import TYPE_CHECKING, Optional

from wexample_helpers.classes.extended_base_model import ExtendedBaseModel

if TYPE_CHECKING:
    from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse
    from wexample_prompt.common.prompt_context import PromptContext


class AbstractOutputHandler(ExtendedBaseModel):
    def print(self, response: "AbstractPromptResponse", context: Optional["PromptContext"] = None) -> None:
        ...
