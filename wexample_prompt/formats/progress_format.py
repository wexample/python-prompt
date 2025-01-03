from wexample_prompt.formats.base_format import BaseFormat
from wexample_prompt.enums.response_type import ResponseType
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment


class ProgressFormat(BaseFormat):
    """Format for displaying progress bars."""
    
    @classmethod
    def create(cls, total: int, current: int, width: int = 50) -> 'ProgressFormat':
        """Create a progress bar response.
        
        Args:
            total: Total number of items
            current: Current progress
            width: Width of the progress bar in characters
        """
        percentage = min(100, int(100 * current / total))
        filled = int(width * current / total)
        
        bar = "[" + "=" * filled + " " * (width - filled) + "]"
        text = f"{bar} {percentage}%"
        
        return cls(
            lines=[PromptResponseLine(segments=[PromptResponseSegment(text=text)])],
            response_type=ResponseType.PROGRESS,
            metadata={"total": total, "current": current, "width": width}
        )
