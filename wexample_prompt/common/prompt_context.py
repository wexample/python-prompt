from typing import ClassVar, Optional

from pydantic import Field
from wexample_helpers.classes.extended_base_model import ExtendedBaseModel
from wexample_helpers.const.types import Kwargs
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.enums.verbosity_level import VerbosityLevel


class PromptContext(ExtendedBaseModel):
    DEFAULT_COLORIZED: ClassVar[bool] = True
    DEFAULT_VERBOSITY: ClassVar[VerbosityLevel] = VerbosityLevel.DEFAULT
    DEFAULT_WIDTH: ClassVar[int] = 80

    """Context for rendering responses, including terminal information."""
    colorized: Optional[bool] = Field(
        default=True, description="Allow to return avoid coloration special characters"
    )
    parent_context: Optional["PromptContext"] = Field(
        default=None, description="A parent context"
    )
    indentation: Optional[int] = Field(default=0, description="Base indentation level")
    indentation_character: Optional[str] = Field(
        default=" ", description="The character used for indentation"
    )
    indentation_color: Optional[TerminalColor] = Field(
        default=None, description="The indentation part color"
    )
    indentation_length: Optional[int] = Field(
        default=2, description="Number of characters to repeat for one indentation"
    )
    verbosity: Optional[VerbosityLevel] = Field(
        default=DEFAULT_VERBOSITY,
        description="The context verbosity, saying which response to render or not",
    )
    width: Optional[int] = Field(
        default=None,
        description="Context with, basically the terminal with including indentation",
    )
    formatting: Optional[bool] = Field(
        default=False,
        description="Format lines on rendering, should be disabled when passing raw text",
    )

    @classmethod
    def create_from_kwargs(cls, kwargs: Kwargs) -> "PromptContext":
        return PromptContext(
            **kwargs,
        )

    @classmethod
    def create_kwargs_from_context(cls, context: "PromptContext") -> "Kwargs":
        return {
            "indentation": context.indentation,
            "indentation_character": context.indentation_character,
            "indentation_color": context.indentation_color,
            "indentation_length": context.indentation_length,
            "verbosity": context.verbosity,
            "width": context.width,
        }

    @classmethod
    def create_from_parent_context_and_kwargs(
        cls, kwargs: Kwargs, parent_context: Optional["PromptContext"] = None
    ) -> "PromptContext":
        if parent_context:
            kwargs["parent_context"] = parent_context

        return cls.create_from_kwargs(
            kwargs,
        )

    @classmethod
    def create_if_none(
        cls, context: Optional["PromptContext"] = None
    ) -> "PromptContext":
        """
        Creating a context allows to execute render without any extra information,
        but manager parameters like terminal width are not available in this case.
        """
        return context or PromptContext()

    def render_indentation_text(self) -> str:
        output = ""
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
        return self.get_indentation_character() * (
            self.get_indentation() * self.indentation_length
        )

    def get_width(self) -> int:
        # None width allowed to let know that no fixed width has been specified before using it.
        return self.width or PromptContext.DEFAULT_WIDTH

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
