if __name__ == "__main__":
    from wexample_prompt.testing.resources.classes.class_indenation_level_one import ClassIndentationLevelOne

    level_one = ClassIndentationLevelOne()
    level_one._init_io_manager()

    level_one.print_deep_log_one()

    from wexample_prompt.common.io_manager import IoManager
    import time
    from wexample_helpers.const.spinners import BRAILLE_SPINNER_FRAMES as SPINNER_FRAMES
    io = IoManager()
    io.separator()

    frames = SPINNER_FRAMES
    start = time.time()
    total = 5.0  # seconds
    delay = 0.05  # 50 ms between frames
    while time.time() - start < total:
        for sym in frames:
            if time.time() - start >= total:
                break
            response = io.info('Loading...', symbol=sym)
            time.sleep(delay)
            io.erase_response(response=response)
