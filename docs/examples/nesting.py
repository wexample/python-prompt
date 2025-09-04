if __name__ == "__main__":
    from wexample_prompt.testing.resources.classes.class_indenation_level_one import ClassIndentationLevelOne

    level_one = ClassIndentationLevelOne()
    level_one._init_io_manager()

    level_one.print_deep_log_one()

    from wexample_prompt.common.io_manager import IoManager
    import time
    from wexample_prompt.common.spinner_pool import SpinnerPool
    io = IoManager()
    io.separator()

    start = time.time()
    total = 5.0  # seconds
    delay = 0.05  # 50 ms between frames
    while time.time() - start < total:
        sym = SpinnerPool.next()
        response = io.info('Loading...', symbol=sym)
        time.sleep(delay)
        io.erase_response(response=response)
