from typing import Optional

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.mixins.with_io_manager import WithIoManager


class WithIoMethods(
    WithIoManager
):
    def __getattr__(self, name: str):
        if hasattr(self.io, name):
            attr = getattr(self.io, name)

            if callable(attr):
                def wrapper(*args, **kwargs):
                    if args:
                        formatted_msg = self.format_message(args[0])
                        args = (formatted_msg,) + args[1:]
                    return attr(*args, **kwargs)

                return wrapper

            return attr

        return super().__getattr__(name)

    def create_io_context(self) -> Optional["PromptContext"]:
        return None
