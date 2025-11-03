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
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    def _get_io_methods(self, name: str) -> Any:
        io = self.ensure_io_manager()

        if hasattr(io, name):
            attr = getattr(io, name)
            if callable(attr):

                def wrapper(*args, **kwargs):
                    if "context" not in kwargs or kwargs["context"] is None:
                        kwargs["context"] = self.create_io_context()
                    
                    # Add prefix to message if defined
                    prefix = self.get_io_context_prefix()
                    if prefix and "message" in kwargs:
                        prefix_format = self.get_io_context_prefix_format()
                        formatted_prefix = prefix_format.format(prefix=prefix)
                        kwargs["message"] = formatted_prefix + kwargs["message"]
                    elif prefix and len(args) > 0 and isinstance(args[0], str):
                        # Handle positional message argument
                        prefix_format = self.get_io_context_prefix_format()
                        formatted_prefix = prefix_format.format(prefix=prefix)
                        args = (formatted_prefix + args[0],) + args[1:]
                    
                    return attr(*args, **kwargs)

                return wrapper
            return attr
        return None
