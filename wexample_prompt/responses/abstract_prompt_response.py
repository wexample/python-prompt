from abc import ABC
from typing import TYPE_CHECKING

from pydantic import BaseModel

from wexample_helpers.classes.mixin.has_snake_short_class_name_class_mixin import HasSnakeShortClassNameClassMixin

if TYPE_CHECKING:
    pass


class AbstractPromptResponse(HasSnakeShortClassNameClassMixin, BaseModel, ABC):
    pass

    def render(self) -> str:
        """Render the complete response."""
        return "TODO"