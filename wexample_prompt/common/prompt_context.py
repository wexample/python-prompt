from pydantic import BaseModel, Field


class PromptContext(BaseModel):
    color_enabled: bool = Field(
        default=True,
        description="Allow to return avoid coloration special characters"
    )
