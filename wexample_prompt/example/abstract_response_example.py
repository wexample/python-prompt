from abc import abstractmethod
from typing import TYPE_CHECKING, Optional

from wexample_helpers.classes.extended_base_model import ExtendedBaseModel
from wexample_prompt.mixins.with_io_manager import WithIoManager

if TYPE_CHECKING:
    from wexample_prompt.example.example_class_with_methods import ExampleClassWithMethods
    from wexample_prompt.common.io_manager import IoManager


class AbstractResponseExample(WithIoManager, ExtendedBaseModel):
    _class_with_methods: Optional["ExampleClassWithMethods"] = None

    def __init__(self, io: Optional["IoManager"] = None, **kwargs):
        from wexample_prompt.example.example_class_with_methods import ExampleClassWithMethods

        ExtendedBaseModel.__init__(self, **kwargs)
        WithIoManager.__init__(self, io=io)

        self._init_io_manager()
        self._class_with_methods = ExampleClassWithMethods(io=self._io)

    @abstractmethod
    def example_class(self):
        pass

    @abstractmethod
    def example_manager(self):
        pass

    @abstractmethod
    def example_extended(self) -> None:
        pass
