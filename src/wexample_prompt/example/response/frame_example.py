from __future__ import annotations

from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class FrameExample(AbstractResponseExample):
    """Example for the rounded-corner frame response."""

    def example_class(self):
        from wexample_prompt.responses.frame_prompt_response import FramePromptResponse

        return FramePromptResponse.create_frame(
            text=["Welcome to wex prompt", "This is a framed message."],
            title="Hello",
        )

    def example_extended(self) -> None:
        self._class_with_methods.frame(
            text="Frame called from a class with io methods.",
            title="Extended",
        )

    def example_manager(self) -> None:
        self.io.frame(
            text="Frame called directly from the io manager.",
            title="Manager",
        )

    def example_with_color(self) -> None:
        from wexample_prompt.enums.terminal_color import TerminalColor

        self.io.frame(
            text=["Border in cyan.", "Content keeps its own styling."],
            title="Colored Border",
            border_color=TerminalColor.CYAN,
        )

    def example_no_title(self) -> None:
        self.io.frame(
            text="A frame without any title.",
        )

    def example_nested_responses(self) -> None:
        from wexample_prompt.responses.log_prompt_response import LogPromptResponse
        from wexample_prompt.responses.messages.info_prompt_response import (
            InfoPromptResponse,
        )
        from wexample_prompt.responses.messages.success_prompt_response import (
            SuccessPromptResponse,
        )

        info = InfoPromptResponse.create_info(message="Status: nominal.")
        log = LogPromptResponse.create_log(message="Reading config file...")
        success = SuccessPromptResponse.create_success(message="All checks passed.")

        self.io.frame(
            responses=[info, log, success],
            title="Startup",
        )

    def example_multiline_text(self) -> None:
        self.io.frame(
            text=(
                "Line one.\n"
                "Line two with a slightly longer text.\n"
                "Line three."
            ),
            title="Multi-line",
        )

    def get_examples(self) -> list[dict[str, Any]]:
        return [
            {
                "title": "Simple",
                "description": "Frame with title and short text",
                "callback": self.example_manager,
            },
            {
                "title": "No title",
                "description": "Frame without a title",
                "callback": self.example_no_title,
            },
            {
                "title": "Colored border",
                "description": "Border with cyan color",
                "callback": self.example_with_color,
            },
            {
                "title": "Nested responses",
                "description": "Frame wrapping info/log/success responses",
                "callback": self.example_nested_responses,
            },
            {
                "title": "Multi-line text",
                "description": "Frame with a string containing line breaks",
                "callback": self.example_multiline_text,
            },
        ]
