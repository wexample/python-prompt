from pydantic import BaseModel, Field


class PromptContext(BaseModel):
    colorized: bool = Field(
        default=True,
        description="Allow to return avoid coloration special characters"
    )
    indentation: int = Field(
        default=0,
        description="Base indentation level"
    )
    indentation_spaces_count: int = Field(
        default=2,
        description="Number of spaces for one indentation"
    )

    def get_indentation(self) -> str:
        """Get the current indentation string."""
        return " " * (self.indentation * self.indentation_spaces_count)
