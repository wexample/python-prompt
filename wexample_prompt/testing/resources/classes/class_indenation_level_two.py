from typing import TYPE_CHECKING

from wexample_prompt.mixins.with_io_context import WithIoContext
from wexample_prompt.mixins.with_io_manager import WithIoManager

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext


class ClassIndentationLevelTwo(WithIoManager, WithIoContext):
    def __init__(self, io, parent_context: "PromptContext", **kwargs):
        from wexample_prompt.common.prompt_context import PromptContext
        WithIoManager.__init__(self, io=io)

        self._io_context = PromptContext(
            indentation=parent_context.indentation + 1,
            colorized=parent_context.colorized,
        )

    def print_deep_log_two(self):
        from wexample_prompt.testing.resources.classes.class_indenation_level_three import ClassIndentationLevelThree

        self.io.log(
            message='test deep log two',
            context=self._io_context
        )

        level_two = ClassIndentationLevelThree(
            io=self.io,
            parent_context=self._io_context
        )

        return level_two.print_deep_log_three()
