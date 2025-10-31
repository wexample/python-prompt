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


def section_nested_sub_progress(io: IoManager) -> None:
    io.separator('Nested sub progress (multi-level)')
    response = io.progress(label='Global task', total=1000)
    root = response.get_handle()

    # Initialize global
    root.update(current=100, label="Global: initial")

    # Level 1 sub-range within the global range
    lvl1 = root.create_range_handle(to=600)
    lvl1.update(current="20%", label="Level 1: update")

    # Level 2 sub-range within level 1
    lvl2 = lvl1.create_range_handle(to=500)
    lvl2.advance(step="50%", label="Level 2: advance")

    # Level 3 sub-range within level 2
    lvl3 = lvl2.create_range_handle(to=450)
    lvl3.update(current="75%", label="Level 3: update")
    lvl3.finish(label="Level 3: finish", color=TerminalColor.CYAN)

    # Finish upwards
    lvl2.finish(label="Level 2: finish")
    lvl1.finish(label="Level 1: finish", color=TerminalColor.MAGENTA)
    root.finish(color=TerminalColor.RED, label="Global: finished")


def section_dynamic_resize_sub_progress(io: IoManager) -> None:
    io.separator('Dynamic resize of sub progress (change total/to after creation)')
    response = io.progress(label='Global task', total=1000)
    root = response.get_handle()

    # Start somewhere
    root.update(current=100, label="Global: initial")

    # Create a sub-range initially of size 200 (100 -> 300)
    child = root.create_range_handle(to=300)
    child.update(current=50, label="Child before resize")

    # Now decide the child will actually need a total of 400 units instead of 200
    # Option 1: via update(total=...)
    child.update(total=400, label="Child resized via total=400")
    # Continue within the resized range
    child.update(current=200, label="Child mid after resize")

    # Option 2: direct property assignment (equivalent)
    child.total = 500  # expands the child to map 100 -> 600 on parent
    child.update(current=500, label="Child end after property resize")
    child.finish(color=TerminalColor.YELLOW, label="Child finished")

    # Finish global
    root.finish(color=TerminalColor.RED, label="Global: finished")


def section_virtual_subdivisions(io: IoManager) -> None:
    io.separator('Virtual subdivisions (3 main items, 6 substeps each)')
    # Simulate processing 3 main items, each subdivided into 6 substeps
    # Total should reach 100% after all items are processed
    response = io.progress(label='Processing items', total=3)
    root = response.get_handle()

    for item_idx in range(3):  # 3 main items
        root.context.indentation += 1
        # Reserve 1 unit on parent bar starting from current position
        # from_ is omitted so it defaults to current parent position
        # virtual_total=6 means we can count 6 steps that map to 1 parent unit
        sub = root.create_range_handle(
            to_step=1,  # Reserve 1 unit on parent from current position
            virtual_total=6,  # Virtual total: 6 substeps within 1 parent unit
            # indentation=10
        )
        
        for step in range(1, 7):
            sleep(0.05)
            sub.advance(
                step=1,
                label=f"Item {item_idx + 1}/3, substep {step}/6"
            )
        
        # Finish the sub-range to move parent to the end of this range
        sub.finish()
        root.context.indentation -= 1
    
    # Finish the root to reach 100%
    root.finish(label="All items complete", color=TerminalColor.GREEN)


if __name__ == "__main__":
    io = IoManager()
    section_using_io_manager(io)
    section_standalone_no_manager()
    section_various_inputs(io)
    section_sub_progress(io)
    section_nested_sub_progress(io)
    section_dynamic_resize_sub_progress(io)
    section_virtual_subdivisions(io)
