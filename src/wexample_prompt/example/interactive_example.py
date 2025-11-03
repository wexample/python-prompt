from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.example.example import Example

from wexample_prompt.mixins.with_io_methods import WithIoMethods

if TYPE_CHECKING:
    from wexample_prompt.example.interactive_executor import InteractiveExecutor


class InteractiveExample(Example, WithIoMethods):
    def bind_executor(self, executor: "InteractiveExecutor") -> None:
        object.__setattr__(self, "executor", executor)
        object.__setattr__(self, "parent_io_handler", executor)
        object.__setattr__(self, "io", executor.io)

    def before_execute(self) -> None:
        """Hook executed before example logic."""

    def after_execute(self) -> None:
        """Hook executed after example logic."""

    def run(self) -> None:
        """Run the example with optional pre/post hooks."""
        self.before_execute()
        self.execute()
        self.after_execute()
