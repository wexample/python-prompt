from wexample_helpers.classes.extended_base_model import ExtendedBaseModel
from wexample_prompt.mixins.with_required_io_manager import WithRequiredIoManager


class ExtendedBaseModelWithRequiredIoManager(WithRequiredIoManager, ExtendedBaseModel):
    """
    The minimal class with an io manager.
    """
