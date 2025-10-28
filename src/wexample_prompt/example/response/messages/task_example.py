from __future__ import annotations

from wexample_helpers.decorator.base_class import base_class
from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class TaskExample(AbstractResponseExample):
    def example_class(self):
        from wexample_prompt.responses.messages.task_prompt_response import (
            TaskPromptResponse,
        )

        return TaskPromptResponse.create_task(
            message=self.get_test_message(),
        )

    def example_extended(self) -> None:
        self._class_with_methods.task(message=self.get_test_message())

    def example_manager(self) -> None:
        self.io.task(message=self.get_test_message())

    def get_test_message(self) -> str:
        return "Test task message"
