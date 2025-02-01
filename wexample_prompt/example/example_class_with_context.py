from pydantic import BaseModel

from wexample_prompt.mixins.with_prompt_context import WithPromptContext


class ExampleClassWithContext(WithPromptContext, BaseModel):
    pass
