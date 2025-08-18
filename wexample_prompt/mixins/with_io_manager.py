from typing import Optional, Any

from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.terminal_color import TerminalColor


class WithIoManager:
    _io: Optional[IoManager] = None
    _io_context_colorized: Optional[bool] = None
    _io_context: "PromptContext"
    _io_parent_context: "Any" = None

    def __init__(
            self,
            io: Optional[IoManager] = None,
            parent_io_handler: "WithIoManager" = None,
    ) -> None:
        if parent_io_handler and isinstance(parent_io_handler, WithIoManager):
            self._io_parent_context = parent_io_handler.io_context
            self._io = parent_io_handler.io
        else:
            self._io = io
        self._io_context = self._create_io_context()

    @property
    def io(self) -> IoManager:
        return self._io

    @io.setter
    def io(self, manager: IoManager) -> None:
        """Set the IoManager instance."""
        self._io = manager

    @property
    def io_context(self) -> "PromptContext":
        return self._io_context

    def _init_io_manager(self) -> None:
        self._io = IoManager()

    def _create_io_context(self, **kwargs) -> "PromptContext":
        defaults = {
            "parent_context": self._io_parent_context,
            "indentation": self.get_io_context_indentation(),
            "indentation_character": self.get_io_context_indentation_character(),
            "indentation_color": self.get_io_context_indentation_color(),
            "colorized": self.get_io_context_colorized()
                         or (self._io_parent_context.colorized if self._io_parent_context is not None else True),
        }

        defaults.update(kwargs)

        return PromptContext.create_from_kwargs(
            kwargs=defaults,
        )

    def get_io_context_colorized(self) -> Optional[bool]:
        return None

    def get_io_context_indentation(self) -> Optional[int]:
        return None

    def get_io_context_indentation_character(self) -> Optional[str]:
        return None

    def get_io_context_indentation_color(self) -> Optional[TerminalColor]:
        return None
