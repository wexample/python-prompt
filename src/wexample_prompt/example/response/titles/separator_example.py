from __future__ import annotations

from wexample_prompt.example.abstract_response_example import AbstractResponseExample

from wexample_helpers.decorator.base_class import base_class
@base_class
class SeparatorExample(AbstractResponseExample):
    def example_class(self):
        from wexample_prompt.responses.titles.separator_prompt_response import (
            SeparatorPromptResponse,
        )

        return SeparatorPromptResponse.create_separator("From response")

    def example_extended(self) -> None:
        self._class_with_methods.separator(label="Class method")

    def example_manager(self) -> None:
        self.io.separator()
