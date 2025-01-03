#!/usr/bin/env python3

from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.text_style import TextStyle
from wexample_prompt.responses import (
    BasePromptResponse,
    TablePromptResponse,
    ListPromptResponse,
    TreePromptResponse,
    ProgressPromptResponse
)
from wexample_prompt.responses.messages import (
    AlertPromptResponse,
    CriticalPromptResponse,
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


def demo_progress():
    """Demonstrate progress bar."""
    print("\n=== Progress Bar ===")
    for i in range(0, 101, 20):
        progress = ProgressPromptResponse.create(100, i)
        print(progress.render() + "\r", end="", flush=True)
        import time
        time.sleep(0.5)
    print()


def demo_message_types():
    """Demonstrate different message types."""
    print("\n=== Message Types ===")
    messages = [
        AlertPromptResponse.create("This is an alert message"),
        CriticalPromptResponse.create("This is a critical message"),
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


if __name__ == "__main__":
    print("=== Prompt Response Demo ===")
    demo_styles()
    demo_table()
    demo_list()
    demo_tree()
    demo_progress()
    demo_message_types()
