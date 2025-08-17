from typing import TYPE_CHECKING, Optional

from wexample_helpers.classes.extended_base_model import ExtendedBaseModel
from wexample_prompt.mixins.with_io_context import WithIoContext
from wexample_prompt.mixins.with_required_io_manager import WithRequiredIoManager

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext


class ClassIndentationLevelThree(WithRequiredIoManager, WithIoContext, ExtendedBaseModel):
    def __init__(self, io, parent_io_context: "PromptContext", **kwargs):
        ExtendedBaseModel.__init__(self, **kwargs)
        WithRequiredIoManager.__init__(self, io=io)
        WithIoContext.__init__(
            self,
            parent_io_context=parent_io_context
        )

    def get_io_context_indentation_character(self) -> Optional[str]:
        return "·"

    def print_deep_log_three(self):
        return self.io.log(
            message='test deep log three',
            context=self._io_context
        )
