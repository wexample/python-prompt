from pydantic import BaseModel, Field


class PromptContext(BaseModel):
    colorized: bool = Field(
        default=True,
        description="Allow to return avoid coloration special characters"
    )
