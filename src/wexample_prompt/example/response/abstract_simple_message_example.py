"""Abstract base class for simple message examples (echo, log, info, debug, etc.)."""

from __future__ import annotations

from typing import Any

from wexample_helpers.decorator.base_class import base_class
from wexample_prompt.enums.terminal_bg_color import TerminalBgColor
from wexample_prompt.enums.terminal_color import TerminalColor

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class AbstractSimpleMessageExample(AbstractResponseExample):
    """Base class for simple message examples with standard formatting tests."""

    def example_normal(self) -> None:
        """Normal message without formatting."""
        method = self.get_io_method()
        name = self.get_response_name()
        method(message=f"Simple {name} message")

    def example_formatted(self) -> None:
        """Message with color and bold formatting."""
        method = self.get_io_method()
        method(message="@color:cyan{Cyan text}")
        method(message="@color:yellow+bold{Bold yellow text}")
        method(message="@🔵{Blue emoji} with @color:magenta+bold{mixed} @color:green{formatting}")

    def example_emoji(self) -> None:
        """Message with emojis."""
        method = self.get_io_method()
        method(message="🎉 Success with emoji")
        method(message="⚠️ Warning emoji 🔥 Fire emoji")
        method(message="@color:cyan{Colored text} with 🌟 emoji 🚀 inside")
        method(message="Multiple emojis: 🔵 🟢 🟡 🔴 🟣 🟠")

    def example_inline_styling(self) -> None:
        """Message with inline styling (underline, italic, etc.)."""
        method = self.get_io_method()
        method(message="Text with @🟣+underline{underline styling}")
        method(message="Text with @color:yellow+italic{italic styling}")
        method(message="@color:cyan+bold{Bold} and @color:magenta+underline{underline} and @color:green+italic{italic}")
        method(message="@🔵+bold+underline{Multiple styles combined}")

    def example_edge_cases(self) -> None:
        """Message with edge cases: very short, very long, special characters."""
        method = self.get_io_method()
        
        # Very short
        method(message="OK")
        method(message="✓")
        
        # Very long
        long_text = "This is a very long message that contains a lot of text to test how the prompt system handles wrapping and display of lengthy content. " * 3
        method(message=long_text)
        
        # Special characters
        method(message="Special chars: <>&\"'`[]{}()±×÷≠≈∞")
        method(message="Path: /home/user/very/long/path/to/some/file/that/might/wrap.txt")
        method(message="URL: https://example.com/very/long/url/with/many/segments?param1=value1&param2=value2")

    def example_nesting(self) -> None:
        """Message with nested parent/child classes demonstrating automatic indentation."""
        from wexample_helpers.decorator.base_class import base_class
        from wexample_prompt.enums.indentation_style import IndentationStyle
        from wexample_prompt.enums.terminal_color import TerminalColor
        from wexample_prompt.mixins.with_io_methods import WithIoMethods
        
        method = self.get_io_method()
        
        # Parent class
        @base_class
        class ParentTask(WithIoMethods):
            def execute(self):
                self.log("Parent task started")
                self.log("Processing parent operations...")
                
                # Create child with automatic indentation
                child = ChildTask(parent_io_handler=self)
                child.execute()
                
                self.log("Parent task completed")
        
        # Child class
        @base_class
        class ChildTask(WithIoMethods):
            def execute(self):
                self.log("Child task started")
                self.log("Processing child operations...")
                
                # Create grandchild with automatic indentation
                grandchild = GrandchildTask(parent_io_handler=self)
                grandchild.execute()
                
                self.log("Child task completed")
        
        # Grandchild class with custom indentation style
        @base_class
        class GrandchildTask(WithIoMethods):
            def get_io_context_indentation_style(self):
                return IndentationStyle.VERTICAL
            
            def get_io_context_indentation_character(self) -> str:
                return "│"
            
            def get_io_context_indentation_text_color(self):
                return TerminalColor.CYAN
            
            def execute(self):
                self.log("Grandchild task started (vertical style)")
                self.log("Processing grandchild operations...")
                self.log("Grandchild task completed")
        
        # Execute the demo
        method(message="@color:yellow+bold{Nesting Demo: Parent/Child/Grandchild}")
        parent = ParentTask(io=self.io)
        parent.execute()

    def example_indented(self) -> None:
        """Message with indentation."""
        from wexample_prompt.enums.indentation_style import IndentationStyle
        from wexample_prompt.enums.terminal_bg_color import TerminalBgColor
        from wexample_prompt.enums.terminal_color import TerminalColor
        
        method = self.get_io_method()
        name = self.get_response_name()
        
        # Normal indentation (repeat mode - default)
        method(message=f"Normal {name}", indentation=0)
        method(message=f"Indented {name} (level 3)", indentation=3)
        method(message=f"Indented {name} (level 5)", indentation=5)
        
        # Colored indentation text
        method(
            message=f"@color:cyan{{Colored {name} with indentation}}",
            indentation=3,
            indentation_text_color=TerminalColor.CYAN
        )
        
        # Colored indentation background
        method(
            message=f"@🔵+bold{{Colored background indentation}}",
            indentation=5,
            indentation_bg_color=TerminalBgColor.BLUE,
        )
        
        # Custom indentation character (repeat mode)
        method(
            message=f"Custom character (repeat mode)",
            indentation=4,
            indentation_character="→"
        )
        
        # Vertical style (IDE-like)
        method(
            message=f"@🟢+bold{{Vertical style (level 3)}}",
            indentation=3,
            indentation_style=IndentationStyle.VERTICAL,
            indentation_character="│"
        )
        
        # Vertical style with color
        method(
            message=f"@color:magenta+bold{{Vertical with color}}",
            indentation=5,
            indentation_style=IndentationStyle.VERTICAL,
            indentation_character="│",
            indentation_text_color=TerminalColor.MAGENTA
        )
        
        # Vertical style with background color
        method(
            message=f"@color:yellow+bold{{Vertical with bg color}}",
            indentation=4,
            indentation_style=IndentationStyle.VERTICAL,
            indentation_character="┃",
            indentation_bg_color=TerminalBgColor.GREEN
        )

    def get_examples(self) -> list[dict[str, Any]]:
        """Get list of examples.

        Returns:
            List of example configurations
        """
        return [
            {
                "title": "Normal",
                "description": "Simple message without formatting",
                "callback": self.example_normal,
            },
            {
                "title": "Formatted",
                "description": "Message with colors and bold",
                "callback": self.example_formatted,
            },
            {
                "title": "Emoji",
                "description": "Message with various emojis",
                "callback": self.example_emoji,
            },
            {
                "title": "Inline Styling",
                "description": "Message with underline, italic, and combined styles",
                "callback": self.example_inline_styling,
            },
            {
                "title": "Edge Cases",
                "description": "Very short, very long, and special characters",
                "callback": self.example_edge_cases,
            },
            {
                "title": "Nesting",
                "description": "Parent/child classes with automatic indentation",
                "callback": self.example_nesting,
            },
            {
                "title": "Indented",
                "description": "Message with various indentation levels",
                "callback": self.example_indented,
            },
        ]
