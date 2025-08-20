from time import sleep

from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.responses.interactive.confirm_prompt_response import ConfirmPromptResponse
from wexample_prompt.responses.interactive.screen_prompt_response import ScreenPromptResponse

if __name__ == "__main__":
    io = IoManager()

    counter = {"n": 0}

    total = 50


    def _callback(response: ScreenPromptResponse):
        response.clear()

        response.print(f"Some text, {counter['n']} times...")
        response.progress(total=total, current=counter["n"], label="Demo progression...")
        response.log(f"(Any io method work)")

        if counter["n"] == 10:
            response.confirm(
                question="Do you want to continue demo ?",
                choices=ConfirmPromptResponse.MAPPING_PRESET_YES_NO,
                default="yes"
            )

            if response.get_answer() == "no":
                response.close()
                return

        sleep(.1)
        counter["n"] += 1
        if counter["n"] > total:
            response.close()
        else:
            response.reload()


    io.screen(callback=_callback, height=10)
