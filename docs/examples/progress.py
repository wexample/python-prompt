from time import sleep

from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.interactive.progress_prompt_response import ProgressPromptResponse


def section_using_io_manager(io: IoManager) -> None:
    io.separator('Using IoManager (managed output)')
    response = io.progress(label='Downloading assets', total=100, current=0)
    handle = response.get_handle()
    for cur in (25, 50, 75, 100):
        sleep(0.1)
        handle.update(
            current=cur,
            label='Downloading…',
            color=(None if cur <= 50 else TerminalColor.YELLOW),
        )


def section_standalone_no_manager() -> None:
    print("\n--- Standalone (no IoManager) ---")
    response = ProgressPromptResponse.create_progress(
        label='Processing tasks', total=80, current=0, color=TerminalColor.CYAN
    )
    # Initial render
    print(response.render() or "")
    handle = response.get_handle()
    for cur in (10, 20, 40, 60, 80):
        sleep(0.1)
        print(
            handle.update(
                current=cur,
                label='Processing…',
                color=(None if cur <= 50 else TerminalColor.MAGENTA),
            )
            or ""
        )


def section_various_inputs(io: IoManager) -> None:
    io.separator('Various inputs (int, float, percent)')
    response = io.progress(label='Progress', total=100)
    handle = response.get_handle()
    handle.update(current="10%", color=TerminalColor.CYAN, label="Set percentage")
    handle.advance(step="1%", label="Advance by percentage")
    handle.update(current="15.325%", color=TerminalColor.YELLOW, label="Set precise percentage")
    handle.advance(step=21.5, label="Advance by units")
    handle.finish(color=TerminalColor.RED, label="Finish")


def section_sub_progress(io: IoManager) -> None:
    io.separator('Sub progress (range handle)')
    response = io.progress(label='Global task', total=1000)
    handle = response.get_handle()
    # Start global progress
    handle.update(current=50, label="Global: initial")

    # Create sub-range: maps a child range to a segment of the parent
    range_handle = handle.create_range_handle(to=350)

    # Update within range
    range_handle.update(current=50, label="Sub-range: update")

    # Advance within the sub-range
    range_handle.advance(step="50%", label="Sub-range: advance")

    # Finish the sub-range
    range_handle.finish(label="Sub-range complete", color=TerminalColor.MAGENTA)

    # Complete the global task
    handle.finish(color=TerminalColor.RED, label="Global: finished")


if __name__ == "__main__":
    io = IoManager()
    section_using_io_manager(io)
    section_standalone_no_manager()
    section_various_inputs(io)
    section_sub_progress(io)
