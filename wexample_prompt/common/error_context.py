from wexample_prompt.common.prompt_context import PromptContext
from pydantic import Field
from typing import Optional, Dict, Any
import traceback


class ErrorContext(PromptContext):
    """Context for error messages."""

    fatal: bool = Field(
        default=False,
        description="Whether this is a fatal error that should exit the program"
    )
    trace: bool = Field(
        default=True,
        description="Whether to show stack trace"
    )
    params: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Parameters to format the message with"
    )
    exit_code: int = Field(
        default=1,
        description="Exit code to use when fatal is True"
    )
    indentation: int = Field(
        default=0,
        description="Indentation level for the message"
    )

    def format_message(self, message: str) -> str:
        message = super().format_message(message)

        if self.trace:
            trace = traceback.format_exc()
            if trace and trace != 'NoneType: None\n':
                message = f"{message}{self._format_traceback(trace)}"

        return message

    def _format_traceback(self, trace: str) -> str:
        """Format a traceback string with visual delimiters.

        Args:
            trace: The traceback string to format

        Returns:
            Formatted traceback string
        """
        if not trace:
            return ""

        lines = trace.strip().split('\n')
        formatted_lines = []

        # Add top delimiter
        formatted_lines.append("┌─" + "─" * 78)
        formatted_lines.append("│ Traceback:")
        formatted_lines.append("├─" + "─" * 78)

        # Format each line of the trace
        for line in lines:
            formatted_lines.append(f"│ {line}")

        # Add bottom delimiter
        formatted_lines.append("└─" + "─" * 78)

        return "\n".join(formatted_lines)
