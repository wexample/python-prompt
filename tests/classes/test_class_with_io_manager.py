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

    def test_instantiate_required_io_manager(self):
        from wexample_prompt.testing.resources.classes.class_with_required_io_manager import ClassWithRequiredIoManager

        # Missing required 'io' should raise a TypeError from __init__
        with self.assertRaises(TypeError):
            # Missing argument
            ClassWithRequiredIoManager()

        # Providing io should work
        instance = ClassWithRequiredIoManager(io=self.io)
        assert isinstance(instance.io, IoManager)
