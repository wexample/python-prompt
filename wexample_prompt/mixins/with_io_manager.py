from typing import Optional
from pydantic import BaseModel, PrivateAttr

from wexample_prompt.io_manager import IoManager


class WithIoManager(BaseModel):
    """
    Mixin that adds an IoManager property to a class.
    The IoManager instance can be shared between multiple classes
    or be unique to each instance.
    """
    
    _io: Optional[IoManager] = PrivateAttr(default=None)
    
    @property
    def io(self) -> IoManager:
        """
        Get the IoManager instance. If none exists, creates a new one.
        
        Returns:
            IoManager: The IoManager instance
        """
        if self._io is None:
            self._io = IoManager()
        return self._io
    
    @io.setter
    def io(self, manager: IoManager) -> None:
        """
        Set the IoManager instance.
        Useful for sharing the same IoManager between multiple classes.
        
        Args:
            manager (IoManager): The IoManager instance to use
        """
        self._io = manager
