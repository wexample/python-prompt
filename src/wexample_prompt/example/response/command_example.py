from __future__ import annotations

from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class CommandExample(AbstractResponseExample):
    """Example for the command response."""

    def example_class(self):
        from wexample_prompt.responses.command_prompt_response import (
            CommandPromptResponse,
        )

        return CommandPromptResponse.create_command(command="ls -la")

    def example_executed(self) -> None:
        self.io.command(
            command="npm install",
            output="added 152 packages in 8s",
            executed=True,
        )

    def example_extended(self) -> None:
        self._class_with_methods.command(command="echo hello")

    def example_manager(self) -> None:
        self.io.command(command="ls -la")

    def example_python_repl(self) -> None:
        self.io.command(command="print('hello')", prompt_char=">>>")

    def example_root_shell(self) -> None:
        self.io.command(command="systemctl restart nginx", prompt_char="#")

    def example_with_output(self) -> None:
        self.io.command(
            command="ls -la",
            output=(
                "total 24\n"
                "drwxr-xr-x  4 weeger weeger 4096 May 25 14:32 .\n"
                "drwxr-xr-x 18 weeger weeger 4096 May 24 09:11 ..\n"
                "-rw-r--r--  1 weeger weeger  340 May 25 14:30 README.md"
            ),
        )

    def get_examples(self) -> list[dict[str, Any]]:
        return [
            {
                "title": "Simple",
                "description": "A command to run",
                "callback": self.example_manager,
            },
            {
                "title": "With output",
                "description": "Command with multi-line output below",
                "callback": self.example_with_output,
            },
            {
                "title": "Executed",
                "description": "Command marked as already executed (green ✓)",
                "callback": self.example_executed,
            },
            {
                "title": "Python REPL",
                "description": "Custom prompt char '>>>'",
                "callback": self.example_python_repl,
            },
            {
                "title": "Root shell",
                "description": "Custom prompt char '#'",
                "callback": self.example_root_shell,
            },
        ]
