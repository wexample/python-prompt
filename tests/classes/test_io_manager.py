class TestIoManager:
    def test_instantiate_io_manager(self):
        from wexample_prompt.common.io_manager import IoManager

        manager = IoManager()
        assert manager is not None
