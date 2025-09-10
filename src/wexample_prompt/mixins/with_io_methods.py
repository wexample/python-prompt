from __future__ import annotations

from typing import Any

from wexample_helpers.decorator.base_class import base_class
from wexample_prompt.mixins.with_io_manager import WithIoManager


@base_class
class WithIoMethods(WithIoManager):
    """
    Allow class to provide Io methods like .log(), .title() etc.
    """

    def __getattr__(self, name: str) -> Any:
        io_response = self._get_io_methods(name)
        if io_response is not None:
            return io_response

        # Try to get the attribute from super(), but handle the case where
        # super() doesn't have __getattr__ (like with attrs classes)
        try:
            return super().__getattr__(name)
        except AttributeError:
            # If super() doesn't have __getattr__, raise AttributeError for the original attribute
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )

    def _get_io_methods(self, name: str) -> Any:
        if hasattr(self.io, name):
            attr = getattr(self.io, name)

            if callable(attr):

                def wrapper(*args, **kwargs):
                    kwargs["context"] = self.io_context
                    return attr(*args, **kwargs)

                return wrapper

            return attr
        return None
