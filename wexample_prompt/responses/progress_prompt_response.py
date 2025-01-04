"""Progress bar response implementation."""
from typing import List, Callable, Optional, Any, ClassVar
import inspect

from wexample_prompt.responses.base_prompt_response import BasePromptResponse
from wexample_prompt.enums.response_type import ResponseType
from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.responses.progress.step_progress_context import (
    ProgressStep,
    StepProgressContext
)


class ProgressPromptResponse(BasePromptResponse):
    """Response for displaying progress bars."""
    
    # Class variables properly annotated for pydantic
    FILL_CHAR: ClassVar[str] = "▰"  # Filled block
    EMPTY_CHAR: ClassVar[str] = "▱"  # Empty block
    
    # ANSI color codes
    CYAN: ClassVar[str] = "\033[36m"
    BLUE: ClassVar[str] = "\033[34m"
    GREEN: ClassVar[str] = "\033[32m"
    RESET: ClassVar[str] = "\033[0m"
    
    @classmethod
    def set_style(cls, fill_char: str = "▰", empty_char: str = "▱"):
        """Set the progress bar style characters.
        
        Args:
            fill_char: Character to use for filled portion
            empty_char: Character to use for empty portion
        """
        cls.FILL_CHAR = fill_char
        cls.EMPTY_CHAR = empty_char
    
    @classmethod
    def create(
        cls,
        total: int,
        current: int,
        width: int = 50,
        label: Optional[str] = None
    ) -> 'ProgressPromptResponse':
        """Create a simple progress bar response.
        
        Args:
            total: Total number of items
            current: Current progress
            width: Width of the progress bar in characters
            label: Optional label to show above the progress bar
            
        Raises:
            ValueError: If total or current are negative, or if width is less than 1
            ZeroDivisionError: If total is zero
        """
        if total <= 0:
            raise ValueError("Total must be greater than 0")
        if current < 0:
            raise ValueError("Current progress cannot be negative")
        if width < 1:
            raise ValueError("Width must be at least 1")
            
        # Cap current at total
        current = min(current, total)
        
        percentage = min(100, int(100 * current / total))
        filled = int(width * current / total)
        
        # Choose color based on progress
        if percentage < 33:
            color = cls.BLUE
        elif percentage < 66:
            color = cls.CYAN
        else:
            color = cls.GREEN
            
        # Build progress bar without brackets
        bar = (
            color +
            cls.FILL_CHAR * filled +
            cls.EMPTY_CHAR * (width - filled) +
            cls.RESET
        )
        
        # If we have a label, include the progress bar on the same line
        if label:
            text = f"{label} {bar} {percentage}%"
            segments = [PromptResponseSegment(text=text)]
        else:
            text = f"{bar} {percentage}%"
            segments = [PromptResponseSegment(text=text)]
            
        return cls(
            lines=[PromptResponseLine(segments=segments)],
            response_type=ResponseType.PROGRESS,
            metadata={
                "total": total,
                "current": current,
                "width": width,
                "label": label
            }
        )
    
    @classmethod
    def create_steps(
        cls,
        steps: List[ProgressStep],
        width: int = 50,
        title: Optional[str] = None
    ) -> StepProgressContext:
        """Create a step-based progress context.
        
        Args:
            steps: List of progress steps to execute
            width: Width of the progress bar
            title: Optional title for the progress bar
            
        Returns:
            StepProgressContext to be used in a with statement
        """
        total_weight = sum(step.weight for step in steps)
        return StepProgressContext(
            steps=steps,
            total_weight=total_weight,
            width=width,
            title=title
        )
    
    @classmethod
    def execute(
        cls,
        callbacks: List[Callable[..., Any]],
        width: int = 50,
        title: Optional[str] = None
    ) -> List[Any]:
        """Execute a list of callbacks with progress tracking.
        
        This is a simplified version that takes just a list of callback functions.
        It automatically extracts descriptions from docstrings or function names.
        
        Args:
            callbacks: List of callback functions to execute
            width: Width of the progress bar
            title: Optional title for the progress bar
            
        Returns:
            List of results from each callback
            
        Example:
            ```python
            ProgressPromptResponse.execute([
                step1,
                step2,
                step3
            ])
            ```
        """
        # Convert callbacks to ProgressSteps
        steps = []
        for callback in callbacks:
            # Try to get description from docstring
            desc = inspect.getdoc(callback)
            if not desc:
                # Fall back to function name
                desc = callback.__name__.replace('_', ' ').capitalize()
            else:
                # Take first line of docstring
                desc = desc.split('\n')[0]
                
            steps.append(ProgressStep(
                callback=callback,
                description=desc,
                weight=1.0  # Equal weight for all steps
            ))
            
        # Use the context manager internally
        with cls.create_steps(steps, width, title) as progress:
            return progress.execute_steps()
