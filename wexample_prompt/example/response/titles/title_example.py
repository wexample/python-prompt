from wexample_prompt.example.abstract_response_example import AbstractResponseExample
from wexample_prompt.responses.titles.title_prompt_response import TitlePromptResponse


class TitleExample(AbstractResponseExample):
    def get_test_message(self) -> str:
        return "Test title"

    def example_manager(self):
        self.io.title(message=self.get_test_message())

    def example_class(self):
        return TitlePromptResponse.create_title(
            text=self.get_test_message() + ' (from response)'
        )

    def example_extended(self):
        self._class_with_methods.title(
            message=self.get_test_message() + ' (class method)'
        )
