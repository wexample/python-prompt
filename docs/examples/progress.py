from time import sleep

from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.interactive.progress_prompt_response import ProgressPromptResponse

if __name__ == "__main__":
    demo_io = IoManager()

    demo_io.separator('Introduction')
    demo_io.log(f'This is a {"long " * 100}message that shows you the terminal width')

    demo_io.separator('Using IoManager')
    response = demo_io.progress(
        label='Progress via IoManager',
        total=100,
        current=0
    )
    handle = response.get_handle()
    for cur in (25, 50, 75, 100):
        sleep(0.1)
        handle.update(current=cur, label=f"Io progress {cur}%", color=(None if cur <= 50 else TerminalColor.YELLOW))

    demo_io.separator('Standalone (no terminal info)')
    response = ProgressPromptResponse.create_progress(
        label='Progress without IoManager',
        total=80,
        current=0,
        color=TerminalColor.CYAN
    )

    # First render
    print(response.render() or "")
    handle2 = response.get_handle()
    for cur in (10, 20, 40, 60, 80):
        sleep(0.1)
        print(handle2.update(
            current=cur,
            label=f"Standalone {cur}/{response.total}",
            color=(None if cur <= 50 else TerminalColor.MAGENTA)
        ))

    demo_io.separator('Test dirct finishing')
    response = demo_io.progress(label='Progress via IoManager', total=100)
    response.get_handle().finish(color=TerminalColor.RED)
