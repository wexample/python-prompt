"""Example for debug response."""
from wexample_prompt.example.abstract_response_example import AbstractResponseExample
from wexample_prompt.responses.messages.debug_prompt_response import DebugPromptResponse


class DebugExample(AbstractResponseExample):
    """Example class for debug responses."""

    def example_class(self):
        """Example using the class directly."""
        DebugPromptResponse.create_debug(
            'Test debug message',
            context=self.io_manager.create_context()
        )

    def example_manager(self):
        """Example using IoManager."""
        self.io_manager.debug('Test debug message')

    def example_context(self):
        """Example using PromptContext."""
        self.class_with_context.debug('Test debug message')
