from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any

from wexample_helpers.classes.base_class import BaseClass

from wexample_helpers.decorator.base_class import base_class
if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.responses.abstract_prompt_response import (
        AbstractPromptResponse,
    )


@base_class
class AbstractOutputHandler(BaseClass):
    @abstractmethod
    def erase(
            self,
            response: AbstractPromptResponse,
    ) -> Any:
        self._raise_not_implemented_error()

    @abstractmethod
    def print(
            self,
            response: AbstractPromptResponse,
            context: PromptContext | None = None,
    ) -> Any:
        self._raise_not_implemented_error()
