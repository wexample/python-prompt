from wexample_prompt.testing.abstract_prompt_response_test import AbstractPromptResponseTest


class TestIoManager(AbstractPromptResponseTest):
    def setUp(self):
        """Set up common test fixtures."""
        super().setUp()

    def test_class_indentation_levels(self):
        from wexample_prompt.testing.resources.classes.class_indenation_level_one import ClassIndentationLevelOne
        level_one = ClassIndentationLevelOne(io=self._io)
        level_one.print_deep_log_one()

        assert level_one is not None
