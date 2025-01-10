from typing import Optional
from pydantic import BaseModel, Field

from wexample_prompt.io_manager import IoManager


class WithIoManager(BaseModel):
    io: Optional[IoManager] = Field(
        default=None,
        description="IoManager instance that can be injected via constructor"
    )
    
    @property
    def io(self) -> IoManager:
        if self.io is None:
            self.io = IoManager()
        return self.io
    
    @io.setter
    def io(self, manager: IoManager) -> None:
        self.io = manager
