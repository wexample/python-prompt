import subprocess
import time
from time import sleep

from wexample_helpers.classes.example.example import Example
from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.responses.interactive.confirm_prompt_response import ConfirmPromptResponse
from wexample_prompt.responses.interactive.screen_prompt_response import ScreenPromptResponse


class ScreenExample(Example):
    def execute(self) -> None:
        io = IoManager()

        counter = {"n": 0}
        total = 50

        def _callback(response: ScreenPromptResponse):
            response.clear()

            response.print(f"@color:cyan+bold{{Some text}}, {counter['n']} times...")
            response.progress(
                total=total, current=counter["n"], label="@color:yellow{Demo progression...}"
            )
            response.log("@🟢{(Any io method works)}")

            if counter["n"] == 10:
                response.confirm(
                    question="@🔵+bold{Do you want to continue demo ?}",
                    choices=ConfirmPromptResponse.MAPPING_PRESET_YES_NO,
                    default="yes",
                )

                if response.get_answer() == "no":
                    response.close()
                    return

            sleep(0.01)
            counter["n"] += 1
            if counter["n"] > total:
                response.close()
            else:
                response.reload()

        io.screen(callback=_callback, height=10)

        # --- Minimal shell-based demo: show moving process data for ~10 seconds ---
        start = time.time()

        def _proc_callback(response: ScreenPromptResponse):
            response.clear()
            response.print("@color:magenta+bold{Top CPU processes (refresh 1s, ~10s total)}")

            # Get processes sorted by CPU descending; keep header + 10 rows
            cmd = ["ps", "-eo", "pid,comm,pcpu,pmem,etime", "--sort=-pcpu"]
            res = subprocess.run(cmd, capture_output=True, text=True, check=False)
            lines = [ln for ln in res.stdout.strip().splitlines() if ln.strip()]
            for ln in lines[:11]:
                response.print(f"@color:cyan{{{ln}}}")

            if time.time() - start >= 3:
                response.close()
                return

            sleep(1.0)
            response.reload()

        io.screen(callback=_proc_callback, height=14)
