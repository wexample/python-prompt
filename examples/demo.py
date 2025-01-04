#!/usr/bin/env python3

from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.enums.text_style import TextStyle
from wexample_prompt.io_manager import IOManager
from wexample_prompt.responses import (
    BasePromptResponse,
    TablePromptResponse,
    ListPromptResponse,
    TreePromptResponse,
    MainTitleResponse,
    SubtitleResponse,
    ProgressPromptResponse
)
from wexample_prompt.responses.messages import (
    DebugPromptResponse,
    ErrorPromptResponse,
    FailurePromptResponse,
    InfoPromptResponse,
    LogPromptResponse,
    SuccessPromptResponse,
    TaskPromptResponse,
    WarningPromptResponse
)
from wexample_prompt.responses.progress import ProgressStep


def demo_styles(io: IOManager):
    """Demonstrate different text styles."""
    title = MainTitleResponse.create("Text Styles")
    io.print_response(title)
    
    segments = [
        PromptResponseSegment(text="Normal, "),
        PromptResponseSegment(text="Bold, ", styles=[TextStyle.BOLD]),
        PromptResponseSegment(text="Italic, ", styles=[TextStyle.ITALIC]),
        PromptResponseSegment(text="Bold+Italic", styles=[TextStyle.BOLD, TextStyle.ITALIC]),
    ]
    line = PromptResponseLine(segments=segments)
    response = BasePromptResponse(lines=[line])
    io.print_response(response)


def demo_table(io: IOManager):
    """Demonstrate table formatting."""
    title = MainTitleResponse.create("Table Format")
    io.print_response(title)
    
    # Simple table with headers
    io.print_response(InfoPromptResponse.create("Simple table with headers:"))
    data = [
        ["John", "30", "New York"],
        ["Jane", "25", "San Francisco"],
        ["Bob", "35", "Chicago"]
    ]
    headers = ["Name", "Age", "City"]
    table = TablePromptResponse.create(data, headers=headers)
    io.print_response(table)
    
    # Table with title
    io.print_response(InfoPromptResponse.create("Table with title:"))
    data = [
        ["Python", "High", "Web, Data, AI"],
        ["JavaScript", "High", "Web, Frontend"],
        ["Rust", "Medium", "Systems, CLI"]
    ]
    headers = ["Language", "Usage", "Domains"]
    table = TablePromptResponse.create(
        data,
        headers=headers,
        title="Programming Languages"
    )
    io.print_response(table)
    
    # Table with varying column widths
    io.print_response(InfoPromptResponse.create("Table with varying column widths:"))
    data = [
        ["A short text", "This is a much longer text that will expand the column", "Short"],
        ["Row 2", "More text here", "Data"],
        ["Another row", "Content", "More"]
    ]
    headers = ["Column 1", "Column 2", "Column 3"]
    table = TablePromptResponse.create(data, headers=headers)
    io.print_response(table)
    
    # Table with missing data
    io.print_response(InfoPromptResponse.create("Table with missing data:"))
    data = [
        ["Complete", "Row", "Here"],
        ["Missing", "Data"],
        ["Also", "Incomplete"],
        ["Full", "Row", "Again"]
    ]
    headers = ["Col 1", "Col 2", "Col 3"]
    table = TablePromptResponse.create(data, headers=headers)
    io.print_response(table)


def demo_list(io: IOManager):
    """Demonstrate list formatting."""
    title = MainTitleResponse.create("List Format")
    io.print_response(title)
    
    items = [
        "First item",
        "Second item",
        "Third item with sub-items:",
        "  Sub-item 1",
        "  Sub-item 2",
        "Fourth item",
        "Fifth item with deep nesting:",
        "  Level 2 item",
        "    Level 3 item",
        "      Level 4 item"
    ]
    list_output = ListPromptResponse.create(items)
    io.print_response(list_output)


def demo_tree(io: IOManager):
    """Demonstrate tree structure."""
    title = MainTitleResponse.create("Tree Format")
    io.print_response(title)
    
    data = {
        "root": {
            "folder1": {
                "file1": "content1",
                "file2": "content2"
            },
            "folder2": {
                "file3": "content3"
            }
        }
    }
    tree = TreePromptResponse.create(data)
    io.print_response(tree)


def demo_message_types(io: IOManager):
    """Demonstrate different message types."""
    title = MainTitleResponse.create("Message Types")
    io.print_response(title)
    
    # Show message type examples
    messages = [
        DebugPromptResponse.create("This is a debug message"),
        ErrorPromptResponse.create("This is an error message"),
        FailurePromptResponse.create("Operation failed: Unable to connect"),
        InfoPromptResponse.create("This is an info message"),
        LogPromptResponse.create("This is a log message"),
        SuccessPromptResponse.create("Operation completed successfully"),
        TaskPromptResponse.create("This is a task message"),
        WarningPromptResponse.create("This is a warning message")
    ]
    for message in messages:
        io.print_response(message)


def demo_titles(io: IOManager):
    """Demonstrate title formatting."""
    main = MainTitleResponse.create("Main Title Demo", color=TerminalColor.GREEN)
    io.print_response(main)
    
    sub1 = SubtitleResponse.create("First Subtitle")
    io.print_response(sub1)
    
    sub2 = SubtitleResponse.create("Second Subtitle", color=TerminalColor.MAGENTA)
    io.print_response(sub2)


def demo_indentation(io: IOManager):
    """Demonstrate message indentation."""
    title = MainTitleResponse.create("Message Indentation")
    io.print_response(title)
    
    # Simple indentation example
    log = LogPromptResponse.create("Root level message")
    io.print_response(log)
    
    log.lines[0].indent_level = 1
    io.print_response(log)
    
    # Multiline with indentation
    multiline_msg = (
        "Processing started:\n"
        "  Step 1: Data validation\n"
        "    - Checking formats\n"
        "    - Verifying integrity\n"
        "  Step 2: Transformation\n"
        "    - Applying rules\n"
        "    - Saving results"
    )
    multiline = LogPromptResponse.create(multiline_msg)
    io.print_response(InfoPromptResponse.create("Multiline example:"))
    io.print_response(multiline)


def demo_progress(io: IOManager):
    """Demonstrate progress bar."""
    title = MainTitleResponse.create("Progress Bar")
    io.print_response(title)
    
    # Simple progress bar
    io.print_response(InfoPromptResponse.create("Simple progress bar:"))
    for i in range(0, 101, 20):
        progress = ProgressPromptResponse.create(100, i)
        io.print_response(progress)
        import time
        time.sleep(0.2)
    
    # Progress bar with label
    io.print_response(InfoPromptResponse.create("\nProgress bar with label:"))
    for i in range(0, 101, 20):
        progress = ProgressPromptResponse.create(
            total=100,
            current=i,
            label=f"Processing item {i}/100"
        )
        io.print_response(progress)
        time.sleep(0.2)
    
    # Step-based progress
    io.print_response(InfoPromptResponse.create("\nStep-based progress:"))
    
    def step1():
        """Initialize system."""
        time.sleep(0.5)
        return True
        
    def step2():
        """Load configuration."""
        time.sleep(0.8)
        return True
        
    def step3():
        """Process data."""
        time.sleep(1.2)
        return True
        
    def step4():
        """Save results."""
        time.sleep(0.7)
        return True
    
    steps = [
        ProgressStep(step1, "Initializing system", 1.0),
        ProgressStep(step2, "Loading configuration", 1.5),
        ProgressStep(step3, "Processing data", 2.0),
        ProgressStep(step4, "Saving results", 1.0)
    ]
    
    with ProgressPromptResponse.create_steps(
        steps=steps,
        title="System Setup",
        width=40
    ) as progress:
        progress.execute_steps()


if __name__ == "__main__":
    io = IOManager()
    main = MainTitleResponse.create("Prompt Response Demo", color=TerminalColor.GREEN)
    io.print_response(main)
    
    demo_styles(io)
    demo_table(io)
    demo_list(io)
    demo_tree(io)
    demo_message_types(io)
    demo_titles(io)
    demo_indentation(io)
    demo_progress(io)
