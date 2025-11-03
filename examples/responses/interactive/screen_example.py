import subprocess
import time
from time import sleep

from ..abstract_prompt_response_example import AbstractPromptResponseExample
from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.responses.interactive.confirm_prompt_response import ConfirmPromptResponse
from wexample_prompt.responses.interactive.screen_prompt_response import ScreenPromptResponse


class ScreenExample(AbstractPromptResponseExample):
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

        # === EDGE CASES: LIMITS ===
        io.separator("@🔶+bold{LIMITS: Long text in screen}")

        counter_long = {"n": 0}
        total_long = 20

        def _long_text_callback(response: ScreenPromptResponse):
            response.clear()
            response.print(self.generate_long_single_line_text())
            response.progress(
                total=total_long,
                current=counter_long["n"],
                label="@color:cyan{Processing long text...}"
            )
            
            sleep(0.05)
            counter_long["n"] += 1
            if counter_long["n"] > total_long:
                response.close()
            else:
                response.reload()

        io.screen(callback=_long_text_callback, height=8)

        # === EDGE CASES: INDENTATION ===
        io.separator("@🔶+bold{INDENTATION: Screen with indentation}")

        io.indentation = 3
        counter_indent = {"n": 0}
        total_indent = 15

        def _indented_callback(response: ScreenPromptResponse):
            response.clear()
            response.print("@color:magenta+bold{Indented screen content}")
            response.progress(
                total=total_indent,
                current=counter_indent["n"],
                label="@color:yellow{Progress...}"
            )
            
            sleep(0.05)
            counter_indent["n"] += 1
            if counter_indent["n"] > total_indent:
                response.close()
            else:
                response.reload()

        io.screen(callback=_indented_callback, height=6)
        io.indentation = 0

        # === EDGE CASES: NESTING ===
        io.separator("@🔶+bold{NESTING: Screen with nested prompts}")

        counter_nested = {"n": 0, "confirmed": False}
        total_nested = 30

        def _nested_callback(response: ScreenPromptResponse):
            response.clear()
            response.print("@color:cyan+bold{Nested screen demo}")
            response.print(f"@color:yellow{{Counter: {counter_nested['n']}/{total_nested}}}")
            
            response.progress(
                total=total_nested,
                current=counter_nested["n"],
                label="@color:green{Processing...}"
            )
            
            if counter_nested["n"] == 10 and not counter_nested["confirmed"]:
                result = response.confirm(
                    question="@🔵+bold{Continue processing?}",
                    choices=ConfirmPromptResponse.MAPPING_PRESET_YES_NO,
                    default="yes",
                )
                counter_nested["confirmed"] = True
                
                if response.get_answer() == "no":
                    response.close()
                    return
            
            sleep(0.05)
            counter_nested["n"] += 1
            if counter_nested["n"] > total_nested:
                response.close()
            else:
                response.reload()

        io.screen(callback=_nested_callback, height=10)
