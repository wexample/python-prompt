"""Base prompt response class."""
from typing import TYPE_CHECKING

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse

if TYPE_CHECKING:
    pass


class BasePromptResponse(AbstractPromptResponse):
    pass
