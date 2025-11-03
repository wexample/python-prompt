from __future__ import annotations

from typing import Iterable

from wexample_helpers.classes.example.executor import Executor

from wexample_prompt.example.interactive_example import InteractiveExample
from wexample_prompt.mixins.with_io_manager import WithIoManager
from wexample_prompt.mixins.with_io_methods import WithIoMethods


class InteractiveExecutor(Executor, WithIoMethods):
    """
    Executor variant that leverages the prompt IO manager to render progress,
    separators, and messages while running examples.
    """

    def __attrs_post_init__(self) -> None:
        # Ensure an IO manager is available before parent init instantiates examples.
        self._init_io_manager()
        object.__setattr__(self, "parent_io_handler", None)
        super().__attrs_post_init__()
        self._attach_examples_to_executor()

    def _attach_examples_to_executor(self) -> None:
        """
        Bind every discovered example to this executor so they share the same IO manager.
        """
        examples_registry = self.get_registry("examples")

        for example in examples_registry.get_all().values():
            if hasattr(example, "executor"):
                object.__setattr__(example, "executor", self)

            if isinstance(example, WithIoManager):
                object.__setattr__(example, "parent_io_handler", self)
                object.__setattr__(example, "io", self.io)

            if isinstance(example, InteractiveExample):
                example.bind_executor(self)

    def execute(self) -> None:
        examples_registry = self.get_registry("examples")
        matched = False

        for index, (key, example) in enumerate(examples_registry.get_all().items(), start=1):
            if not self._should_run_example(key, example):
                continue

            matched = True
            self.separator(label=f"@🔷+bold{{{key}}}")
            self.log(message=f"@color:cyan{{Executing example #{index}}}")

            runner = getattr(example, "run", None)
            if callable(runner):
                runner()
            else:
                example.execute()

        if self.filters and not matched:
            tokens: Iterable[str] = self.filters or ()
            filters = ", ".join(tokens)
            self.warning(message=f"No examples matched filters: {filters}")
