from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.testing.abstract_prompt_response_test import AbstractPromptResponseTest


class TestIoManager(AbstractPromptResponseTest):
    def setUp(self):
        """Set up common test fixtures."""
        super().setUp()

    def test_instantiate_io_manager(self):
        from wexample_prompt.testing.resources.classes.class_with_io_manager import ClassWithIoManager

        instance = ClassWithIoManager()
        assert instance.io is None

        instance = ClassWithIoManager(io=self.io)
        assert isinstance(instance.io, IoManager)
