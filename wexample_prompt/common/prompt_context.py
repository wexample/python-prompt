from pydantic import Field

from wexample_helpers.classes.extended_base_model import ExtendedBaseModel


class PromptContext(ExtendedBaseModel):
    colorized: bool = Field(
        default=True,
        description="Allow to return avoid coloration special characters"
    )
    indentation: int = Field(
        default=0,
        description="Base indentation level"
    )
    indentation_character: str = Field(
        default=" ",
        description="The character used for indentation"
    )
    indentation_length: int = Field(
        default=2,
        description="Number of characters to repeat for one indentation"
    )

    def get_indentation(self) -> str:
        """Get the current indentation string."""
        return self.indentation_character * (self.indentation * self.indentation_length)
