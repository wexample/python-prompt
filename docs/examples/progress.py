from wexample_prompt.common.io_manager import IoManager
from time import sleep
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.responses.interactive.progress_prompt_response import ProgressPromptResponse
from wexample_prompt.enums.terminal_color import TerminalColor

if __name__ == "__main__":
    demo_io = IoManager()

    demo_io.log(f'This is a {"long " * 100}message that shows you the terminal width')

    # 1) Using IoManager.progress (one-shot start), then updating via the response handle
    resp = demo_io.progress(
        label='Progress via IoManager',
        total=100,
        current=0
    )
    handle = resp.get_handle()
    for cur in (25, 50, 75, 100):
        sleep(0.1)
        handle.update(current=cur, label=f"Io progress {cur}%")

    # 2) Without IoManager: create, render, then update via handle
    ctx = PromptContext()
    resp2 = ProgressPromptResponse.create_progress(
        label='Progress without IoManager',
        total=80,
        current=0
    )

    # First render
    print(resp2.render(context=ctx) or "")
    handle2 = resp2.get_handle()
    for cur in (10, 20, 40, 60, 80):
        sleep(0.1)
        print(handle2.update(current=cur, label=f"Standalone {cur}/{resp2.total}"))
