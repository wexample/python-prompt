from __future__ import annotations

from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class ChoiceExample(AbstractResponseExample):
    """Example usage of ChoicePromptResponse with edge cases."""

    @staticmethod
    def generate_long_multiline_text() -> str:
        """Generate long multiline text for testing limits."""
        several_lines = "> @color:cyan{And several short lines}\n"
        return (
            "@🔵+bold{This is a }" + ("@color:yellow{long} " * 15) + "text\n"
            "> With a " + ("@color:magenta{long} " * 10) + "line\n" + several_lines * 10
        )

    @staticmethod
    def generate_long_single_line_text() -> str:
        """Generate long single line text for testing wrapping."""
        return (
            "@🔵+bold{This is a }"
            + ("@color:yellow{long} " * 20)
            + "text with @🟣+underline{inline styling} sprinkled everywhere."
        )

    @staticmethod
    def generate_special_characters_text() -> str:
        """Generate text with special characters."""
        return "@🔵{Special: } émojis 🎉 symbols ±×÷ quotes \"'` brackets []{}() slashes /\\"

    def edge_case_indentation(self) -> None:
        """Test edge cases: indentation."""
        self.io.choice(
            question="@🟢+bold{Choice with indentation}",
            choices=["Yes", "No"],
            indentation=5,
            predefined_answer="Yes",
        )

        self.io.indentation = 3
        self.io.choice(
            question="@🟢+bold{Choice with double indentation}",
            choices=["Yes", "No"],
            indentation=5,
            predefined_answer="Yes",
        )
        self.io.indentation = 0

    def edge_case_limits(self) -> None:
        """Test edge cases: limits (long text, many choices)."""
        # Long multiline text
        self.io.choice(
            question=self.generate_long_multiline_text(),
            choices=["Option A", "Option B"],
            predefined_answer="Option A",
        )

        # Long single line
        self.io.choice(
            question=self.generate_long_single_line_text(),
            choices=["Yes", "No"],
            predefined_answer="Yes",
        )

        # Very long choice labels
        self.io.choice(
            question="Select an option with @🔵+bold{very long labels}:",
            choices=[
                "This is a very long choice label that contains a lot of text and should test wrapping",
                "Another extremely long option with lots of words",
                "Short",
            ],
            predefined_answer="Short",
        )

        # Many choices
        many_choices = {f"option_{i}": f"Option {i}" for i in range(1, 21)}
        self.io.choice(
            question="Select from @🔵+bold{many options}:",
            choices=many_choices,
            predefined_answer="option_1",
        )

    def edge_case_special(self) -> None:
        """Test edge cases: special characters."""
        self.io.choice(
            question=self.generate_special_characters_text(),
            choices=[
                "Option with émojis 🎉",
                "Option with symbols ±×÷",
                "Normal option",
            ],
            predefined_answer="Normal option",
        )

    def example_class(self, indentation: int | None = None):
        from wexample_prompt.responses.interactive.choice_prompt_response import (
            ChoicePromptResponse,
        )

        return ChoicePromptResponse.create_choice(
            question="Select an option:",
            choices={
                "value1": "Choice 1",
                "value2": "Choice 2",
                "value3": "Choice 3",
            },
            default="value2",
            predefined_answer="value3",
        )

    def example_extended(self) -> None:
        choices = ["Option 1", "Option 2", "Option 3"]
        self._class_with_methods.choice(
            question="Select an option:", choices=choices, predefined_answer="Option 2"
        )

    def example_manager(self) -> None:
        choices = ["Option 1", "Option 2", "Option 3"]
        self.io.choice(
            question="Select an option:", choices=choices, predefined_answer="Option 2"
        )

    def example_nesting(self) -> None:
        """Choice with parent/child nesting."""
        from wexample_prompt.example.helpers.nesting_demo_classes import ParentTask

        self.io.choice(
            question="@color:yellow+bold{Nesting Demo} - Continue?",
            choices=["Yes", "No"],
            predefined_answer="Yes",
        )
        parent = ParentTask(io=self.io)
        parent.execute(method_name="log")

    def example_simple(self) -> None:
        """Simple yes/no choice."""
        self.io.choice(
            question="Do you want to continue?",
            choices=["Yes", "No"],
            predefined_answer="Yes",
        )

    def example_with_dict(self) -> None:
        """Choice with dict (value: label)."""
        self.io.choice(
            question="Select your preferred language:",
            choices={
                "py": "🐍 Python",
                "js": "📜 JavaScript",
                "rs": "🦀 Rust",
                "go": "🐹 Go",
            },
            default="py",
            predefined_answer="py",
        )

    def example_with_emojis(self) -> None:
        """Choice with emojis."""
        self.io.choice(
            question="🚀 Select action:",
            choices=[
                "✅ Deploy",
                "🧪 Run tests",
                "📊 View stats",
                "❌ Cancel",
            ],
            predefined_answer="🧪 Run tests",
        )

    def example_with_formatting(self) -> None:
        """Choice with inline formatting."""
        self.io.choice(
            question="@color:cyan+bold{Select deployment environment}:",
            choices=[
                "@color:green{Production}",
                "@color:yellow{Staging}",
                "@color:blue{Development}",
            ],
            predefined_answer="@color:blue{Development}",
        )

    def example_with_detail_pane(self) -> None:
        """Choice with a live detail pane (PropertiesPromptResponse) under the list."""
        from wexample_prompt.responses.data.properties_prompt_response import (
            PropertiesPromptResponse,
        )

        agents = {
            "default": {
                "description": "Generalist agent used when no specialty is needed.",
                "model": "claude-opus-4-7",
                "tools": "all",
            },
            "frontend": {
                "description": "Specialist for UI work — knows the design system.",
                "model": "claude-sonnet-4-6",
                "tools": "Read, Edit, Bash",
            },
            "backend": {
                "description": "Database, APIs, infra.",
                "model": "claude-sonnet-4-6",
                "tools": "Read, Edit, Bash, Grep",
            },
        }

        def detail_for(value):
            props = agents.get(value)
            if props is None:
                return None
            return PropertiesPromptResponse.create_properties(
                properties=props, title=str(value).capitalize()
            )

        self.io.choice(
            question="Choose an agent",
            choices={key: key for key in agents},
            detail_provider=detail_for,
            predefined_answer="default",
        )

    def example_with_paths(self) -> None:
        """Choice with file paths."""
        self.io.choice(
            question="Select configuration file:",
            choices=[
                "@path:short{/etc/app/config.yml}",
                "@path:short{/home/user/.config/app.conf}",
                "@path:short{/opt/app/settings.json}",
            ],
            predefined_answer="@path:short{/etc/app/config.yml}",
        )

    def get_examples(self) -> list[dict[str, Any]]:
        """Get list of examples.

        Returns:
            List of example configurations
        """
        return [
            {
                "title": "Simple",
                "description": "Simple yes/no choice",
                "callback": self.example_simple,
            },
            {
                "title": "With Formatting",
                "description": "Choice with inline formatting (@color)",
                "callback": self.example_with_formatting,
            },
            {
                "title": "With Emojis",
                "description": "Choice with emojis",
                "callback": self.example_with_emojis,
            },
            {
                "title": "With Dict",
                "description": "Choice with dict (value: label)",
                "callback": self.example_with_dict,
            },
            {
                "title": "With Paths",
                "description": "Choice with clickable file paths (@path)",
                "callback": self.example_with_paths,
            },
            {
                "title": "With Detail Pane",
                "description": "Live detail pane (properties) under the list, updates on navigation",
                "callback": self.example_with_detail_pane,
            },
            {
                "title": "Nesting",
                "description": "Choice with parent/child nesting",
                "callback": self.example_nesting,
            },
            {
                "title": "Edge Case: Limits",
                "description": "Long text and many choices",
                "callback": self.edge_case_limits,
            },
            {
                "title": "Edge Case: Indentation",
                "description": "Choices with various indentation levels",
                "callback": self.edge_case_indentation,
            },
            {
                "title": "Edge Case: Special Characters",
                "description": "Choices with unicode and special characters",
                "callback": self.edge_case_special,
            },
        ]
