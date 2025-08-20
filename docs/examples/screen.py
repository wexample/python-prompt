from time import sleep

from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.responses.interactive.screen_prompt_response import ScreenPromptResponse


if __name__ == "__main__":
    io = IoManager()

    counter = {"n": 0}

    def _callback(resp: ScreenPromptResponse):
        resp.clear()
        resp.print(f"Some text, {counter['n']} times...")
        sleep(0.1)
        counter["n"] += 1
        if counter["n"] > 50:
            resp.close()
        else:
            resp.reload()

    io.screen(callback=_callback, height=10)
