#!/usr/bin/env python3
from pydantic import BaseModel

from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.mixins.with_prompt_context import WithPromptContext


def demo_title(io: IoManager, class_with_context: WithPromptContext):
    io.title('Test title')
    class_with_context.title('Test title')


class ClassWithContext(WithPromptContext, BaseModel):
    pass


if __name__ == "__main__":
    io = IoManager()
    class_with_context = ClassWithContext(io_manager=io)

    demo_title(io, class_with_context)
