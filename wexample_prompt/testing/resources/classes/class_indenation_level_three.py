from wexample_helpers.classes.extended_base_model import ExtendedBaseModel
from wexample_prompt.mixins.with_required_io_manager import WithRequiredIoManager


class ClassIndentationLevelThree(WithRequiredIoManager, ExtendedBaseModel):
    def __init__(self, io, **kwargs):
        ExtendedBaseModel.__init__(self, **kwargs)
        WithRequiredIoManager.__init__(self, io=io)

    def print_deep_log_three(self):
        return self.io.log('ok')
