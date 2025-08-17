from typing import Optional

from pydantic import Field

from wexample_helpers.classes.extended_base_model import ExtendedBaseModel


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
    indentation_length: Optional[int] = Field(
        default=2,
        description="Number of characters to repeat for one indentation"
    )

    def render_indentation(self) -> str:
        output = ''
        if self.parent_context:
            output = self.parent_context.render_indentation()

        """Get the current indentation string."""
        return output + self.render_indentation_part()

    def render_indentation_part(self) -> str:
        return self.get_indentation_character() * (self.get_indentation() * self.indentation_length)

    def get_indentation(self) -> int:
        if self.indentation is None:
            if self.parent_context:
                return 1
            else:
                return 0

        return self.indentation

    def get_indentation_character(self) -> str:
        if self.indentation_character is None:
            if self.parent_context:
                return self.parent_context.get_indentation_character()
            else:
                return " "

        return self.indentation_character
