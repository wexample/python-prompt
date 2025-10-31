from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.enums.terminal_bg_color import TerminalBgColor
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.enums.verbosity_level import VerbosityLevel

if TYPE_CHECKING:
    from wexample_helpers.const.types import Kwargs

    from wexample_prompt.enums.terminal_bg_color import TerminalBgColor
    from wexample_prompt.enums.terminal_color import TerminalColor
    from wexample_prompt.enums.verbosity_level import VerbosityLevel


@base_class
class PromptContext(BaseClass):
    """Context for rendering responses, including terminal information."""

    DEFAULT_COLORIZED: ClassVar[bool] = True
    DEFAULT_VERBOSITY: ClassVar[VerbosityLevel] = VerbosityLevel.DEFAULT
    DEFAULT_WIDTH: ClassVar[int] = 80
    colorized: bool | None = public_field(
        default=True, description="Allow to return avoid coloration special characters"
    )
    formatting: bool | None = public_field(
        default=False,
        description="Format lines on rendering, should be disabled when passing raw text",
    )
    indentation: int | None = public_field(
        default=0, description="Base indentation level"
    )
    indentation_background_color: TerminalBgColor | None = public_field(
        default=None, description="The indentation part background color"
    )
    indentation_character: str | None = public_field(
        default=" ", description="The character used for indentation"
    )
    indentation_color: TerminalColor | None = public_field(
        default=None, description="The indentation part color"
    )
    indentation_length: int | None = public_field(
        default=2, description="Number of characters to repeat for one indentation"
    )
    parent_context: PromptContext | None = public_field(
        default=None, description="A parent context"
    )
    verbosity: VerbosityLevel = public_field(
        default=VerbosityLevel.DEFAULT,
        description="The context verbosity, saying which response to render or not",
    )
    width: int | None = public_field(
        default=None,
        description="Context with, basically the terminal with including indentation",
    )

    @classmethod
    def create_from_kwargs(cls, kwargs: Kwargs) -> PromptContext:
        return PromptContext(
            **kwargs,
        )

    @classmethod
    def create_from_parent_context_and_kwargs(
        cls, kwargs: Kwargs, parent_context: PromptContext | None = None
    ) -> PromptContext:
        if parent_context:
            kwargs["parent_context"] = parent_context

        return cls.create_from_kwargs(
            kwargs,
        )

    @classmethod
    def create_if_none(cls, context: PromptContext | None = None) -> PromptContext:
        """
        Creating a context allows to execute render without any extra information,
        but manager parameters like terminal width are not available in this case.
        """
        return context or PromptContext()

    @classmethod
    def create_kwargs_from_context(cls, context: PromptContext) -> Kwargs:
        return {
            "indentation": context.indentation,
            "indentation_character": context.indentation_character,
            "indentation_color": context.indentation_color,
            "indentation_background_color": context.indentation_background_color,
            "indentation_length": context.indentation_length,
            "verbosity": context.verbosity,
            "width": context.width,
        }

    def calc_indentation_char_length(self) -> int:
        return self.get_indentation() * self.indentation_length

    def get_indentation(self) -> int:
        if self.indentation is None:
            if self.parent_context:
                return 1
            else:
                return 0

        return self.indentation

    def get_indentation_background_color(self) -> TerminalBgColor | None:
        if self.indentation_background_color is None:
            if self.parent_context:
                return self.parent_context.get_indentation_background_color()
            else:
                return None

        return self.indentation_background_color

    def get_indentation_character(self) -> str:
        if self.indentation_character is None:
            if self.parent_context:
                return self.parent_context.get_indentation_character()
            else:
                return " "

        return self.indentation_character

    def get_indentation_color(self) -> TerminalColor | None:
        if self.indentation_color is None:
            if self.parent_context:
                return self.parent_context.get_indentation_color()
            else:
                return None

        return self.indentation_color

    def get_width(self) -> int:
        # None width allowed to let know that no fixed width has been specified before using it.
        return self.width or PromptContext.DEFAULT_WIDTH

    def render_indentation(self) -> str:
        from wexample_prompt.common.color_manager import ColorManager

        indentation = self.render_indentation_text()

        indentation_color = self.get_indentation_color()
        indentation_background_color = self.get_indentation_background_color()
        if self.colorized and indentation_color or indentation_background_color:
            return ColorManager.colorize(
                text=indentation,
                color=indentation_color,
                bg=indentation_background_color,
            )

        return indentation

    def render_indentation_part(self) -> str:
        return self.get_indentation_character() * (self.calc_indentation_char_length())

    def render_indentation_text(self) -> str:
        output = ""
        if self.parent_context:
            output = self.parent_context.render_indentation_text()

        """Get the current indentation string."""
        return output + self.render_indentation_part()
