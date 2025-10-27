from __future__ import annotations

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class SubtitleExample(AbstractResponseExample):
    def example_class(self):
        from wexample_prompt.responses.titles.subtitle_prompt_response import (
            SubtitlePromptResponse,
        )

        return SubtitlePromptResponse.create_subtitle(
            text=self.get_test_message() + " (from response)"
        )

    def example_extended(self) -> None:
        self._class_with_methods.title(text=self.get_test_message() + " (class method)")

    def example_manager(self) -> None:
        self.io.subtitle(text=self.get_test_message())

    def get_test_message(self) -> str:
        return "Test subtitle"
