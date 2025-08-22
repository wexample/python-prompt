from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Optional

from wexample_helpers.classes.extended_base_model import ExtendedBaseModel

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.responses.abstract_prompt_response import (
        AbstractPromptResponse,
    )


class AbstractOutputHandler(ExtendedBaseModel):
    @abstractmethod
    def print(
        self,
        response: AbstractPromptResponse,
        context: Optional["PromptContext"] = None,
    ) -> Any:
        self._raise_not_implemented_error()
