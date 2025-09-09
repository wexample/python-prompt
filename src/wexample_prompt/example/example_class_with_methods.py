from __future__ import annotations

from wexample_prompt.testing.resources.classes.base_class_with_io_methods import (
    BaseClassWithIoMethods,
)

from wexample_helpers.decorator.base_class import base_class
@base_class
class ExampleClassWithMethods(BaseClassWithIoMethods):
    def _format_context_prompt_message(self, message: str, indent: str) -> str:
        return f"{indent}[EXAMPLE|{self.__class__.__name__}]: {message}"
