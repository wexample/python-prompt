from typing import Optional, TYPE_CHECKING, Any

from wexample_prompt.common.io_manager import IoManager

if TYPE_CHECKING:
    from wexample_prompt.output.abstract_output_handler import AbstractOutputHandler


class WithIoManager:
    _io: Optional[IoManager] = None

    def __init__(self, io: Optional[IoManager] = None) -> None:
        self._io = io

    @property
    def io(self) -> IoManager:
        return self._io

    @io.setter
    def io(self, manager: IoManager) -> None:
        """Set the IoManager instance."""
        self._io = manager

    def _init_io_manager(self, output: Optional["AbstractOutputHandler"] = None) -> None:
        self._io = IoManager(output=output)
