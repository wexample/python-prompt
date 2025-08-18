"""Abstract base class for interactive prompt responses."""
from abc import ABC

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse


class AbstractInteractivePromptResponse(AbstractPromptResponse, ABC):
    """Base for interactive responses (those that may call execute())."""
    pass
