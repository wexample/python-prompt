from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.abstract_method import abstract_method
from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.decorator.base_class import base_class
from wexample_prompt.mixins.with_io_manager import WithIoManager

if TYPE_CHECKING:
    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.example.example_class_with_methods import (
        ExampleClassWithMethods,
    )


@base_class
class AbstractResponseExample(WithIoManager, BaseClass):
    _class_with_methods: ExampleClassWithMethods | None = None

    def __attrs_post_init__(self, io: IoManager | None = None, **kwargs) -> None:
        from wexample_prompt.example.example_class_with_methods import (
            ExampleClassWithMethods,
        )

        self._init_io_manager()
        self._class_with_methods = ExampleClassWithMethods(io=self.io)

    @abstract_method
    def example_class(self) -> None:
        pass

    @abstract_method
    def example_extended(self) -> None:
        pass

    @abstract_method
    def example_manager(self) -> None:
        pass
