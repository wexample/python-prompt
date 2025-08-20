from time import sleep

from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.output.buffer_output_handler import BufferOutputHandler
from wexample_prompt.responses.interactive.screen_prompt_response import ScreenPromptResponse


if __name__ == "__main__":
    io = IoManager()

    counter = {"n": 0}

    total = 50

    # Works because we render separately.
    progress_buffer = BufferOutputHandler()
    progress_io = IoManager(output=progress_buffer)
    progress = progress_io.progress(total=total, label="Demo progression...").get_handle()
    progress_buffer.clear()

    def _callback(response: ScreenPromptResponse):
        response.clear()

        response.print(f"Some text, {counter['n']} times...")

        # Global io manager (does not work as it breaks the refresh)
        # io.log(f"Global: Some text, {counter['n']} times...")

        # Local io manager (does not work as it breaks the refresh)
        # local_io = IoManager()
        # local_io.log(f"Local: Some text, {counter['n']} times...")

        # Works because we render separately.
        local_buffer = BufferOutputHandler()
        local_io = IoManager(output=local_buffer)
        local_io.info(f"Local: Some text, {counter['n']} times...")
        response.print(local_buffer.rendered)

        # Works because we render separately.
        progress.update(current=counter["n"])
        response.print(progress_buffer.flush())

        sleep(.1)
        counter["n"] += 1
        if counter["n"] > total:
            response.close()
        else:
            response.reload()

    io.screen(callback=_callback, height=10)
