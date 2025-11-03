from time import sleep

from ..abstract_prompt_response_example import AbstractPromptResponseExample
from wexample_prompt.common.io_manager import IoManager
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.responses.interactive.progress_prompt_response import ProgressPromptResponse


def section_using_io_manager(io: IoManager) -> None:
    io.separator('@🔵+bold{Using IoManager (managed output)}')
    response = io.progress(label='@color:cyan+bold{Downloading assets}', total=100, current=0)
    handle = response.get_handle()
    for cur in (25, 50, 75, 100):
        sleep(0.1)
        handle.update(
            current=cur,
            label='@color:yellow{Downloading…}',
            color=(None if cur <= 50 else TerminalColor.YELLOW),
        )


def section_standalone_no_manager() -> None:
    print("\n--- @color:magenta+bold{Standalone (no IoManager)} ---")
    response = ProgressPromptResponse.create_progress(
        label='@color:cyan+bold{Processing tasks}', total=80, current=0, color=TerminalColor.CYAN
    )
    # Initial render
    print(response.render() or "")
    handle = response.get_handle()
    for cur in (10, 20, 40, 60, 80):
        sleep(0.1)
        print(
            handle.update(
                current=cur,
                label='@color:yellow{Processing…}',
                color=(None if cur <= 50 else TerminalColor.MAGENTA),
            )
            or ""
        )


def section_various_inputs(io: IoManager) -> None:
    io.separator('@🔵+bold{Various inputs (int, float, percent)}')
    response = io.progress(label='@color:cyan{Progress}', total=100)
    handle = response.get_handle()
    handle.update(current="10%", color=TerminalColor.CYAN, label="@color:yellow{Set percentage}")
    handle.advance(step="1%", label="@color:yellow{Advance by percentage}")
    handle.update(current="15.325%", color=TerminalColor.YELLOW, label="@color:yellow{Set precise percentage}")
    handle.advance(step=21.5, label="@color:yellow{Advance by units}")
    handle.finish(color=TerminalColor.RED, label="@🔴+bold{Finish}")


def section_sub_progress(io: IoManager) -> None:
    io.separator('@🔵+bold{Sub progress (range handle)}')
    response = io.progress(label='@color:cyan{Global task}', total=1000)
    handle = response.get_handle()
    # Start global progress
    handle.update(current=50, label="@color:yellow{Global: initial}")

    # Create sub-range: maps a child range to a segment of the parent
    range_handle = handle.create_range_handle(to=350)

    # Update within range
    range_handle.update(current=50, label="@color:yellow{Sub-range: update}")

    # Advance within the sub-range
    range_handle.advance(step="50%", label="@color:yellow{Sub-range: advance}")

    # Finish the sub-range
    range_handle.finish(label="@color:magenta+bold{Sub-range complete}", color=TerminalColor.MAGENTA)

    # Complete the global task
    handle.finish(color=TerminalColor.RED, label="@🔴+bold{Global: finished}")


def section_nested_sub_progress(io: IoManager) -> None:
    io.separator('@🔵+bold{Nested sub progress (multi-level)}')
    response = io.progress(label='@color:cyan{Global task}', total=1000)
    root = response.get_handle()

    # Initialize global
    root.update(current=100, label="@color:yellow{Global: initial}")

    # Level 1 sub-range within the global range
    lvl1 = root.create_range_handle(to=600)
    lvl1.update(current="20%", label="@color:yellow{Level 1: update}")

    # Level 2 sub-range within level 1
    lvl2 = lvl1.create_range_handle(to=500)
    lvl2.advance(step="50%", label="@color:yellow{Level 2: advance}")

    # Level 3 sub-range within level 2
    lvl3 = lvl2.create_range_handle(to=450)
    lvl3.update(current="75%", label="@color:yellow{Level 3: update}")
    lvl3.finish(label="@color:cyan+bold{Level 3: finish}", color=TerminalColor.CYAN)

    # Finish upwards
    lvl2.finish(label="@color:yellow{Level 2: finish}")
    lvl1.finish(label="@color:magenta+bold{Level 1: finish}", color=TerminalColor.MAGENTA)
    root.finish(color=TerminalColor.RED, label="@🔴+bold{Global: finished}")


def section_dynamic_resize_sub_progress(io: IoManager) -> None:
    io.separator('@🔵+bold{Dynamic resize of sub progress (change total/to after creation)}')
    response = io.progress(label='@color:cyan{Global task}', total=1000)
    root = response.get_handle()

    # Start somewhere
    root.update(current=100, label="@color:yellow{Global: initial}")

    # Create a sub-range initially of size 200 (100 -> 300)
    child = root.create_range_handle(to=300)
    child.update(current=50, label="@color:yellow{Child before resize}")

    # Now decide the child will actually need a total of 400 units instead of 200
    # Option 1: via update(total=...)
    child.update(total=400, label="@color:yellow{Child resized via total=400}")
    # Continue within the resized range
    child.update(current=200, label="@color:yellow{Child mid after resize}")

    # Option 2: direct property assignment (equivalent)
    child.total = 500  # expands the child to map 100 -> 600 on parent
    child.update(current=500, label="@color:yellow{Child end after property resize}")
    child.finish(color=TerminalColor.YELLOW, label="@color:yellow+bold{Child finished}")

    # Finish global
    root.finish(color=TerminalColor.RED, label="@🔴+bold{Global: finished}")


def section_virtual_subdivisions(io: IoManager) -> None:
    io.separator('@🔵+bold{Virtual subdivisions (3 main items, 6 substeps each)}')
    # Simulate processing 3 main items, each subdivided into 6 substeps
    # Total should reach 100% after all items are processed
    response = io.progress(label='@color:cyan{Processing items}', total=3)
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
                label=f"@color:yellow{{Item {item_idx + 1}/3, substep {step}/6}}"
            )
        
        # Finish the sub-range to move parent to the end of this range
        sub.finish()
        root.context.indentation -= 1
    
    # Finish the root to reach 100%
    root.finish(label="@🟢+bold{All items complete}", color=TerminalColor.GREEN)

def section_edge_case_limits(io: IoManager) -> None:
    io.separator('@🔶+bold{LIMITS: Long labels in progress bars}')
    
    # Very long label
    response = io.progress(
        label='@color:cyan{This is a very long progress label that contains lots of text and should test wrapping behavior when it exceeds terminal width}',
        total=100
    )
    handle = response.get_handle()
    for cur in (25, 50, 75, 100):
        sleep(0.05)
        handle.update(current=cur)
    
    # Multiple progress bars with varying label lengths
    io.separator('@🔶+bold{LIMITS: Multiple bars with different label lengths}')
    bars = []
    for i in range(3):
        label_length = ['@color:cyan{Short}', '@color:yellow{Medium length label}', '@color:magenta{Very long label that should wrap across multiple lines in the terminal}'][i]
        response = io.progress(label=label_length, total=50, current=0)
        bars.append(response.get_handle())
    
    for cur in range(0, 51, 10):
        sleep(0.05)
        for handle in bars:
            handle.update(current=cur)
    
    for handle in bars:
        handle.finish()


def section_edge_case_indentation(io: IoManager) -> None:
    io.separator('@🔶+bold{INDENTATION: Progress with indentation}')
    
    response = io.progress(
        label='@color:cyan{Level 0}',
        total=100,
        indentation=0
    )
    handle = response.get_handle()
    handle.update(current=50)
    handle.finish()
    
    io.indentation = 3
    response = io.progress(
        label='@color:yellow{Level 3 indentation}',
        total=100
    )
    handle = response.get_handle()
    handle.update(current=50)
    handle.finish()
    
    response = io.progress(
        label='@color:magenta{Level 3 + 5 indentation}',
        total=100,
        indentation=5
    )
    handle = response.get_handle()
    handle.update(current=50)
    handle.finish()
    
    io.indentation = 0


def section_edge_case_nesting_complex(io: IoManager) -> None:
    io.separator('@🔶+bold{NESTING: Complex nested progress with multiple levels}')
    
    # Simulate a complex build process with multiple nested stages
    response = io.progress(label='@color:cyan+bold{Build Process}', total=3)
    root = response.get_handle()
    
    stages = ['Compilation', 'Testing', 'Packaging']
    
    for stage_idx, stage_name in enumerate(stages):
        io.indentation += 1
        stage_handle = root.create_range_handle(
            to_step=1,
            virtual_total=5
        )
        
        for step in range(1, 6):
            sleep(0.03)
            stage_handle.advance(
                step=1,
                label=f"@color:yellow{{{stage_name}: step {step}/5}}"
            )
        
        stage_handle.finish(label=f"@color:green+bold{{{stage_name} complete}}")
        io.indentation -= 1
    
    root.finish(label="@🟢+bold{Build complete}", color=TerminalColor.GREEN)


class ProgressExample(AbstractPromptResponseExample):
    def execute(self) -> None:
        io = IoManager()
        section_using_io_manager(io)
        section_standalone_no_manager()
        section_various_inputs(io)
        section_sub_progress(io)
        section_nested_sub_progress(io)
        section_dynamic_resize_sub_progress(io)
        section_virtual_subdivisions(io)
        
        # Edge cases
        section_edge_case_limits(io)
        section_edge_case_indentation(io)
        section_edge_case_nesting_complex(io)
