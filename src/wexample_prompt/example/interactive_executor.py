from wexample_helpers.classes.example.executor import Executor
from wexample_prompt.example.interactive_example import InteractiveExample
from wexample_prompt.mixins.with_io_methods import WithIoMethods


class InteractiveExecutor(WithIoMethods, Executor):
    def _get_example_class_type(self) -> type[InteractiveExample]:
        return InteractiveExample
