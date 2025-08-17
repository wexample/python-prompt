from wexample_helpers.classes.extended_base_model import ExtendedBaseModel
from wexample_prompt.mixins.with_io_manager import WithIoManager


class ExtendedBaseModelWithIoManager(WithIoManager, ExtendedBaseModel):
    """
    The minimal class with an io manager.
    """
