from wexample_prompt.testing.abstract_prompt_response_test import AbstractPromptResponseTest


class TestIoManager(AbstractPromptResponseTest):
    def setUp(self):
        """Set up common test fixtures."""
        super().setUp()

    def test_instantiate_class(self):
        from wexample_prompt.testing.resources.classes.class_with_io_methods import ClassWithIoMethods

        instance = ClassWithIoMethods(io=self.io)
        assert instance.log(message="test") is not None

    def test_instantiate_extended_base_model(self):
        from wexample_prompt.testing.resources.classes.extended_base_model_with_io_methods import ExtendedBaseModelWithIoMethods

        instance = ExtendedBaseModelWithIoMethods(io=self.io)
        assert instance.log(message="test") is not None
