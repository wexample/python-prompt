from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.enums.terminal_color import TerminalColor

if __name__ == "__main__":
    demo_io = IoManager()

    demo_io.log(f'This is a {"long " * 100}message that shows you the terminal width')

    progress_handle = demo_io.progress(
        label='Starting progress bar',
        total=1000,
        current=0
    ).get_handle()

    progress_handle.advance(step=10)
    progress_handle.advance(step=10)
    progress_handle.advance(step=10)
    progress_handle.advance(step=10)
    progress_handle.advance(step=10)
    progress_handle.advance(step=40, label="Nice progression...")
    progress_handle.advance(step=40, label="Nice progression.....")
    progress_handle.advance(step=40, label="Nice progression.......", color=TerminalColor.YELLOW)
