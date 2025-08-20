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

    demo_io.separator('Test Various')
    response = demo_io.progress(label='Progress', total=100)
    handle = response.get_handle()
    handle.update(current="10%", color=TerminalColor.CYAN, label="Percentage")
    handle.advance(step="1%", label="Percentage advance")
    handle.update(current="15.325%", color=TerminalColor.YELLOW, label="Percentage float")
    handle.advance(step=21.51, label="Float")
    handle.finish(color=TerminalColor.RED, label="Direct finish")

    demo_io.separator('Test sub progress')
    response = demo_io.progress(label='Progress', total=1000)
    handle.update(current=50, label="First progression")
    # Sub progression
    # "from" is optional
    # "current" is optional, by default 0
    # "to" helps to calculate the "total" which is 350 - 50 = 300
    range_handle = handle.create_range_handle(to=350)
    # global handle is now at 100
    range_handle.update(current=50, label="First range progression")
    # global handle is now at 50 + (350 * 0.5) = 2250
    range_handle.advance(step="50%", label="Percentage range advance")
    # The color can be still changed
    range_handle.finish(label="Range complete", color=TerminalColor.MAGENTA)

    # global handle complete.
    handle.finish(color=TerminalColor.RED, label="Direct finish")
