from typing import Optional

from pydantic import Field

from wexample_helpers.classes.extended_base_model import ExtendedBaseModel
from wexample_helpers.const.types import Kwargs
from wexample_prompt.enums.terminal_color import TerminalColor


class PromptContext(ExtendedBaseModel):
    colorized: Optional[bool] = Field(
        default=True,
        description="Allow to return avoid coloration special characters"
    )
    parent_context: Optional["PromptContext"] = Field(
        default=None,
        description="A parent context"
    )
    indentation: Optional[int] = Field(
        default=0,
        description="Base indentation level"
    )
    indentation_character: Optional[str] = Field(
        default=" ",
        description="The character used for indentation"
    )
    indentation_color: Optional[TerminalColor] = Field(
        default=None,
        description="The indentation part color"
    )
    indentation_length: Optional[int] = Field(
        default=2,
        description="Number of characters to repeat for one indentation"
    )
    width: Optional[int] = Field(
        default=80,
        description="Context with, basically the terminal with including indentation"
    )

    @classmethod
    def create_from_kwargs(cls, kwargs: Kwargs) -> "PromptContext":
        return PromptContext(
            **kwargs,
        )

    @classmethod
    def create_from_parent_context_and_kwargs(
            cls,
            kwargs: Kwargs,
            parent_context: Optional["PromptContext"] = None
    ) -> "PromptContext":
        if parent_context:
            kwargs['parent_context'] = parent_context

        return cls.create_from_kwargs(
            kwargs,
        )

    def render_indentation_text(self) -> str:
        output = ''
        if self.parent_context:
            output = self.parent_context.render_indentation()

        """Get the current indentation string."""
        return output + self.render_indentation_part()

    def render_indentation(self) -> str:
        indentation = self.render_indentation_text()

        indentation_color = self.get_indentation_color()
        if self.colorized and indentation_color:
            from wexample_prompt.common.color_manager import ColorManager
            return ColorManager.colorize(indentation, indentation_color)

        return indentation

    def render_indentation_part(self) -> str:
        return self.get_indentation_character() * (self.get_indentation() * self.indentation_length)

    def get_indentation(self) -> int:
        if self.indentation is None:
            if self.parent_context:
                return 1
            else:
                return 0

        return self.indentation

    def get_indentation_color(self) -> Optional[TerminalColor]:
        if self.indentation_color is None:
            if self.parent_context:
                return self.parent_context.get_indentation_color()
            else:
                return None

        return self.indentation_color

    def get_indentation_character(self) -> str:
        if self.indentation_character is None:
            if self.parent_context:
                return self.parent_context.get_indentation_character()
            else:
                return " "

        return self.indentation_character
