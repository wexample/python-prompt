from wexample_prompt.tests.abstract_prompt_response_test import AbstractPromptResponseTest


class TestIoManager(AbstractPromptResponseTest):
    def _instantiate_io_manager(self):
        from wexample_prompt.common.io_manager import IoManager
        return IoManager()

    def test_instantiate_io_manager(self):
        assert self.io is not None

    def test_minimal_log(self):
        assert self.io.log(message="tests") is not None
