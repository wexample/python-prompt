from wexample_prompt.example.abstract_response_example import AbstractResponseExample


class LogExample(AbstractResponseExample):
    def get_test_message(self) -> str:
        return "Test log message"

    def example_manager(self) -> None:
        self.io.log(message=self.get_test_message())

    def example_class(self):
        from wexample_prompt.responses.messages.log_prompt_response import LogPromptResponse
        return LogPromptResponse.create_log(
            message=self.get_test_message(),
        )
