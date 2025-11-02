import time

from wexample_helpers.classes.example.example import Example
from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.common.spinner_pool import SpinnerPool
from wexample_prompt.testing.resources.classes.class_indenation_level_one import (
    ClassIndentationLevelOne,
)


class Nesting(Example):
    def execute(self) -> None:
        level_one = ClassIndentationLevelOne()
        level_one._init_io_manager()
        level_one.print_deep_log_one()

        io = IoManager()
        io.separator("@🔷+bold{Spinner demo}")

        start = time.time()
        total = 5.0  # seconds
        delay = 0.05  # 50 ms between frames
        while time.time() - start < total:
            sym = SpinnerPool.next()
            response = io.info("@🔵{Loading...}", symbol=sym)
            time.sleep(delay)
            io.erase_response(response=response)

        # Custom frames example: use emojis for a fun spinner.
        io.separator("@color:magenta+bold{Custom frames}")
        custom_key = "fun"
        custom_frames = ["🚀", "💣", "😱", "💥", "✨"]
        SpinnerPool.set_frames(custom_frames, key=custom_key)
        start = time.time()
        total = 3.0
        delay = 0.12
        while time.time() - start < total:
            sym = SpinnerPool.next(custom_key)
            response = io.info("@color:yellow+bold{Custom loading...}", symbol=sym)
            time.sleep(delay)
            io.erase_response(response=response)
