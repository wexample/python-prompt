#!/usr/bin/env python3
from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.enums.text_style import TextStyle
from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.io_manager import IoManager
from wexample_prompt.responses import (
    BasePromptResponse,
    TablePromptResponse,
    ListPromptResponse,
    TreePromptResponse,
    MainTitleResponse,
    SubtitleResponse,
    ProgressPromptResponse,
    SuggestionsPromptResponse,
    ChoicePromptResponse,
    ChoiceDictPromptResponse,
    FilePickerPromptResponse,
    DirPickerPromptResponse
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
from InquirerPy.base.control import Choice


def demo_styles(io: IoManager):
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


def demo_table(io: IoManager):
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


def demo_list(io: IoManager):
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


def demo_tree(io: IoManager):
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


def demo_message_types(io: IoManager):
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


def demo_titles(io: IoManager):
    """Demonstrate title formatting."""
    main = MainTitleResponse.create("Main Title Demo", color=TerminalColor.GREEN)
    io.print_response(main)
    
    sub1 = SubtitleResponse.create("First Subtitle")
    io.print_response(sub1)
    
    sub2 = SubtitleResponse.create("Second Subtitle", color=TerminalColor.MAGENTA)
    io.print_response(sub2)


def demo_indentation(io: IoManager):
    """Demonstrate indentation."""
    title = MainTitleResponse.create("Indentation")
    io.print_response(title)
    
    # Show different indentation levels
    io.print_response(InfoPromptResponse.create("No indentation"))
    
    io.log_indent += 1
    io.print_response(InfoPromptResponse.create("One level indent"))
    
    io.log_indent += 1
    io.print_response(InfoPromptResponse.create("Two levels indent"))
    
    # Show indented progress bar
    progress = ProgressPromptResponse.create(
        total=100,
        current=50,
        label="Indented progress"
    )
    io.print_response(progress)
    
    # Reset indentation
    io.log_indent = 0
    io.print_response(InfoPromptResponse.create("Back to no indentation"))


def demo_progress(io: IoManager):
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
    io.print_response(InfoPromptResponse.create("Progress bar with label:"))
    for i in range(0, 101, 20):
        progress = ProgressPromptResponse.create(
            total=100,
            current=i,
            label=f"Processing item {i}/100"
        )
        io.print_response(progress)
        time.sleep(0.2)
    
    # Step-based progress
    io.print_response(InfoPromptResponse.create("Step-based progress:"))
    
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


def demo_suggestions(io: IoManager):
    """Demonstrate suggestions display."""
    io.print_response(
        SuggestionsPromptResponse.create(
            message="You might want to execute one of these commands",
            suggestions=[
                "pip install --upgrade package",
                "python setup.py develop",
                "pytest tests/"
            ]
        )
    )

    # Show single suggestion
    io.print_response(
        SuggestionsPromptResponse.create(
            message="To continue, please run",
            suggestions=["make build"]
        )
    )


def demo_suggestions_verbosity(io: IoManager):
    """Demonstrate verbosity levels with suggestions."""
    # Create contexts with different verbosity levels
    quiet_context = PromptContext(verbosity=VerbosityLevel.QUIET)
    default_context = PromptContext(verbosity=VerbosityLevel.DEFAULT)
    max_context = PromptContext(verbosity=VerbosityLevel.MAXIMUM)
    
    # Create responses with different verbosity requirements
    normal_response = SuggestionsPromptResponse.create(
        message="Standard commands",
        suggestions=["command1", "command2"],
        verbosity=VerbosityLevel.DEFAULT
    )
    
    debug_response = SuggestionsPromptResponse.create(
        message="Debug commands (only shown in maximum verbosity)",
        suggestions=["debug1", "debug2"],
        verbosity=VerbosityLevel.MAXIMUM
    )
    
    # Demonstrate how verbosity affects visibility
    io.print_response(MainTitleResponse.create("Quiet Context (verbosity=0)"))
    normal_response.print(context=quiet_context)  # Won't show
    debug_response.print(context=quiet_context)   # Won't show
    
    io.print_response(MainTitleResponse.create("Default Context (verbosity=1)"))
    normal_response.print(context=default_context)  # Will show
    debug_response.print(context=default_context)   # Won't show
    
    io.print_response(MainTitleResponse.create("Maximum Context (verbosity=3)"))
    normal_response.print(context=max_context)  # Will show
    debug_response.print(context=max_context)   # Will show


def demo_choices(io: IoManager):
    """Demonstrate choice prompts."""
    io.print_response(MainTitleResponse.create("Choice Prompts"))
    
    # Simple list of choices
    choices_response = ChoicePromptResponse.create(
        question="Select your favorite color",
        choices=["Red", "Green", "Blue", "Yellow"]
    )
    io.print_response(choices_response)
    # Note: We don't call execute() in the demo to avoid blocking
    
    # Dictionary choices
    choices_dict = {
        "py": "Python",
        "js": "JavaScript",
        "go": "Golang",
        "rs": "Rust"
    }
    dict_response = ChoiceDictPromptResponse.create(
        question="Select your favorite programming language",
        choices=choices_dict,
        default="py"  # Python as default
    )
    io.print_response(dict_response)
    
    # Choices with Choice objects for more control
    advanced_choices = [
        Choice(value="opt1", name="🚀 Option One - Advanced"),
        Choice(value="opt2", name="⚡ Option Two - Intermediate"),
        Choice(value="opt3", name="🌟 Option Three - Beginner")
    ]
    advanced_response = ChoicePromptResponse.create(
        question="Select difficulty level",
        choices=advanced_choices,
        abort="↩ Go back"
    )
    io.print_response(advanced_response)


def demo_file_pickers(io: IoManager):
    """Demonstrate file and directory pickers."""
    io.print_response(MainTitleResponse.create("File & Directory Pickers"))
    
    # File picker
    file_response = FilePickerPromptResponse.create(
        question="Select a file to open",
        abort="↩ Cancel"
    )
    io.print_response(file_response)
    # Note: We don't call execute() in the demo to avoid blocking
    
    # Directory picker
    dir_response = DirPickerPromptResponse.create(
        question="Select a directory to use",
        abort="↩ Cancel"
    )
    io.print_response(dir_response)


if __name__ == "__main__":
    io = IoManager()
    main = MainTitleResponse.create("Prompt Response Demo", color=TerminalColor.GREEN)
    io.print_response(main)
    
    demo_styles(io)
    demo_table(io)
    demo_list(io)
    demo_tree(io)
    demo_message_types(io)
    demo_titles(io)
    demo_indentation(io)
    demo_suggestions(io)
    demo_suggestions_verbosity(io)
    demo_choices(io)
    demo_file_pickers(io)
    demo_progress(io)