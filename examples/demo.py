#!/usr/bin/env python3

from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.enums.text_style import TextStyle
from wexample_prompt.responses import (
    BasePromptResponse,
    TablePromptResponse,
    ListPromptResponse,
    TreePromptResponse,
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


def demo_styles():
    """Demonstrate different text styles."""
    print("\n=== Text Styles ===")
    segments = [
        PromptResponseSegment(text="Normal, "),
        PromptResponseSegment(text="Bold, ", styles=[TextStyle.BOLD]),
        PromptResponseSegment(text="Italic, ", styles=[TextStyle.ITALIC]),
        PromptResponseSegment(text="Bold+Italic", styles=[TextStyle.BOLD, TextStyle.ITALIC]),
    ]
    line = PromptResponseLine(segments=segments)
    response = BasePromptResponse(lines=[line])
    print(response.render())


def demo_table():
    """Demonstrate table formatting."""
    print("\n=== Table Format ===")
    data = [
        ["Name", "Age", "City"],
        ["John", "30", "New York"],
        ["Jane", "25", "San Francisco"],
        ["Bob", "35", "Chicago"]
    ]
    table = TablePromptResponse.create(data)
    print(table.render())


def demo_list():
    """Demonstrate list formatting."""
    print("\n=== List Format ===")
    items = [
        "First item",
        "Second item",
        "Third item with sub-items:",
        "  • Sub-item 1",
        "  • Sub-item 2"
    ]
    list_output = ListPromptResponse.create(items)
    print(list_output.render())


def demo_tree():
    """Demonstrate tree structure."""
    print("\n=== Tree Format ===")
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
    print(tree.render())


def demo_message_types():
    """Demonstrate different message types."""
    print("\n=== Message Types ===")
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
        print(message.render())


def demo_indentation():
    """Demonstrate message indentation."""
    print("\n=== Message Indentation ===")
    
    # Simple indentation example
    log = LogPromptResponse.create("Root level message")
    print(log.render())
    
    log.lines[0].indent_level = 1
    print(log.render())
    
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
    print("\nMultiline example:")
    print(multiline.render())


def demo_progress():
    """Demonstrate progress bar."""
    print("\n=== Progress Bar ===")
    for i in range(0, 101, 20):
        progress = ProgressPromptResponse.create(100, i)
        print(progress.render() + "\r", end="", flush=True)
        import time
        time.sleep(0.5)
    print()


if __name__ == "__main__":
    demo_styles()
    demo_table()
    demo_list()
    demo_tree()
    demo_message_types()
    demo_indentation()
    demo_progress()
