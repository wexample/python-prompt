from abc import abstractmethod
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel

from wexample_prompt.mixins.with_io_manager import WithIoManager

if TYPE_CHECKING:
    from wexample_prompt.example.example_class_with_context import ExampleClassWithContext
    from wexample_prompt.common.io_manager import IoManager


class AbstractResponseExample(WithIoManager, BaseModel):
    class_with_context: Optional["ExampleClassWithContext"] = None

    def __init__(self, io: Optional["IoManager"] = None, **kwargs):
        from wexample_prompt.example.example_class_with_context import ExampleClassWithContext

        BaseModel.__init__(self, **kwargs)
        WithIoManager.__init__(self, io=io)

        self._init_io_manager()
        self.class_with_context = ExampleClassWithContext(io=self.io)

    @abstractmethod
    def example_class(self, indentation: Optional[int] = None):
        pass

    @abstractmethod
    def example_manager(self):
        pass

    @abstractmethod
    def example_context(self):
        pass
