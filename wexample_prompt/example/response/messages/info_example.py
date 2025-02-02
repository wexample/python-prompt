from wexample_prompt.example.abstract_response_example import AbstractResponseExample
from wexample_prompt.responses.messages.info_prompt_response import InfoPromptResponse


class InfoExample(AbstractResponseExample):

    def example_class(self):
        return InfoPromptResponse.create_info(
            'Test info message',
            context=self.io_manager.create_context()
        )

    def example_manager(self):
        self.io_manager.info('Test info message')

    def example_context(self):
        self.class_with_context.info('Test info message')
