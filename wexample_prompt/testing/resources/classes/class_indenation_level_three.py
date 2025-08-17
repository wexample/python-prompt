from typing import TYPE_CHECKING

from wexample_helpers.classes.extended_base_model import ExtendedBaseModel
from wexample_prompt.mixins.with_io_context import WithIoContext
from wexample_prompt.mixins.with_required_io_manager import WithRequiredIoManager

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext


class ClassIndentationLevelThree(WithRequiredIoManager, WithIoContext, ExtendedBaseModel):
    def __init__(self, io, parent_context: "PromptContext", **kwargs):
        from wexample_prompt.common.prompt_context import PromptContext

        ExtendedBaseModel.__init__(self, **kwargs)
        WithRequiredIoManager.__init__(self, io=io)

        self._io_context = PromptContext(
            indentation=parent_context.indentation + 1,
            colorized=parent_context.colorized,
        )

    def print_deep_log_three(self):
        return self.io.log(
            message='test deep log three',
            context=self._io_context
        )
