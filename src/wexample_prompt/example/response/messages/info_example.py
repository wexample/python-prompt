from __future__ import annotations

from wexample_prompt.example.abstract_response_example import AbstractResponseExample

from wexample_helpers.decorator.base_class import base_class
@base_class
class InfoExample(AbstractResponseExample):
    def example_class(self):
        from wexample_prompt.responses.messages.info_prompt_response import (
            InfoPromptResponse,
        )

        return InfoPromptResponse.create_info(
            message=self.get_test_message(),
        )

    def example_extended(self) -> None:
        self._class_with_methods.info(message=self.get_test_message())

    def example_manager(self) -> None:
        self.io.info(message=self.get_test_message())

    def get_test_message(self) -> str:
        return "Test info message"
