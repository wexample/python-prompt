from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.mixins.with_io_manager import WithIoManager


class WithRequiredIoManager(WithIoManager):
    """Mixin that requires an IoManager instance."""

    def __init__(
            self,
            io: IoManager,
            parent_io_context: "PromptContext" = None,
    ) -> None:
        super().__init__(
            io=io,
            parent_io_context=parent_io_context
        )
