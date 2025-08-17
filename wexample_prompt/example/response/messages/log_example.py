from typing import Optional

from wexample_prompt.example.abstract_response_example import AbstractResponseExample
from wexample_prompt.responses.messages.log_prompt_response import LogPromptResponse


class LogExample(AbstractResponseExample):

    def example_class(self, indentation: Optional[int] = None):
        return LogPromptResponse.create_log(
            'Test log message',
        )

    def example_manager(self):
        self.io.log('Test log message')
