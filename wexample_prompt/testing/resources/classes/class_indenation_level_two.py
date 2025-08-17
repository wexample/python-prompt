from typing import TYPE_CHECKING

from wexample_prompt.mixins.with_io_methods import WithIoMethods

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext


class ClassIndentationLevelTwo(WithIoMethods):
    def __init__(self, io, parent_io_context: "PromptContext"):
        WithIoMethods.__init__(self, io=io, parent_io_context=parent_io_context)

    def print_deep_log_two(self):
        from wexample_prompt.testing.resources.classes.class_indenation_level_three import ClassIndentationLevelThree

        self.log(
            message='test deep log two',
            context=self._io_context
        )

        level_two = ClassIndentationLevelThree(
            io=self.io,
            parent_io_context=self._io_context
        )

        level_two.print_deep_log_three()

        context = self._create_io_context(self._io_context.parent_context)
        context.colorized = False

        level_two = ClassIndentationLevelThree(
            io=self.io,
            parent_io_context=context
        )

        return level_two.print_deep_log_three(context)
