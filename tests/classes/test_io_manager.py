class TestIoManager:
    def _instantiate_io_manager(self):
        from wexample_prompt.common.io_manager import IoManager
        return IoManager()

    def test_instantiate_io_manager(self):
        manager = self._instantiate_io_manager()
        assert manager is not None

    def test_minimal_log(self):
        manager = self._instantiate_io_manager()
        assert manager.log(message="tests") is not None
