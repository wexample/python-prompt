#!/usr/bin/env python3

from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.text_style import TextStyle
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.responses import (
    BasePromptResponse,
    TablePromptResponse,
    ListPromptResponse,
    TreePromptResponse,
    ProgressPromptResponse
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
    for msg_type in MessageType:
        segment = PromptResponseSegment(text=f"This is a {msg_type.value} message")
        line = PromptResponseLine(segments=[segment], line_type=msg_type)
        response = BasePromptResponse(lines=[line], message_type=msg_type)
        print(response.render())


if __name__ == "__main__":
    print("=== Prompt Response Demo ===")
    demo_styles()
    demo_table()
    demo_list()
    demo_tree()
    demo_progress()
    demo_message_types()
