from wexample_helpers.classes.example.executor import Executor
from wexample_prompt.mixins.with_io_methods import WithIoMethods


class InteractiveExecutor(WithIoMethods, Executor):
    pass