from typing import TYPE_CHECKING, Optional

from wexample_helpers.classes.extended_base_model import ExtendedBaseModel
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.mixins.with_required_io_manager import WithRequiredIoManager

if TYPE_CHECKING:
    from wexample_prompt.mixins.with_io_manager import WithIoManager


class ClassIndentationLevelThree(WithRequiredIoManager, ExtendedBaseModel):
    def __init__(self, parent_io_handler: "WithIoManager", **kwargs):
        ExtendedBaseModel.__init__(self, **kwargs)
        WithRequiredIoManager.__init__(
            self,
            io=parent_io_handler.io,
            parent_io_handler=parent_io_handler
        )

    def get_io_context_indentation_character(self) -> Optional[str]:
        return "·"

    def get_io_context_indentation_color(self) -> Optional[TerminalColor]:
        return TerminalColor.BLUE

    def print_deep_log_three(self):
        return self.io.log(
            message='test deep log three',
            context=self.io_context
        )
