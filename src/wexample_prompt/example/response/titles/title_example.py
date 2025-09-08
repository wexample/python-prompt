from __future__ import annotations

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


class TitleExample(AbstractResponseExample):

    def example_class(self):
        from wexample_prompt.responses.titles.title_prompt_response import (
            TitlePromptResponse,
        )

        return TitlePromptResponse.create_title(
            text=self.get_test_message() + " (from response)"
        )

    def example_extended(self) -> None:
        self._class_with_methods.title(text=self.get_test_message() + " (class method)")

    def example_manager(self) -> None:
        self.io.title(text=self.get_test_message())
    def get_test_message(self) -> str:
        return "Test title"
