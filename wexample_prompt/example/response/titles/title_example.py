from wexample_prompt.example.abstract_response_example import AbstractResponseExample
from wexample_prompt.responses.titles.title_prompt_response import TitlePromptResponse


class TitleExample(AbstractResponseExample):

    def example_class(self):
        TitlePromptResponse.create_title(
            'Test title',
            context=self.io_manager.create_context()
        )

    def example_manager(self):
        self.io_manager.title('Test title')

    def example_context(self):
        self.class_with_context.title('Test title')
