"""Step-based progress context implementation."""
from typing import List, Any, Optional, TypeVar, Generic, Callable
from dataclasses import dataclass
import time

# Type variable for step function return type
T = TypeVar('T')


@dataclass
class ProgressStep(Generic[T]):
    """Represents a single step in a progress sequence."""
    callback: Callable[..., T]
    description: str
    weight: float = 1.0


class StepProgressContext:
    """Context manager for step-based progress."""
    
    def __init__(
        self,
        steps: List[ProgressStep],
        total_weight: float,
        width: int = 50,
        title: Optional[str] = None
    ):
        """Initialize the progress context.
        
        Args:
            steps: List of steps to execute
            total_weight: Total weight of all steps
            width: Progress bar width
            title: Optional title
        """
        self.steps = steps
        self.total_weight = total_weight
        self.width = width
        self.title = title
        self.current_weight = 0.0
        self.start_time = 0.0
        
    def __enter__(self) -> 'StepProgressContext':
        """Start the progress context."""
        self.start_time = time.time()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up after progress is complete."""
        pass
        
    def execute_steps(self) -> List[Any]:
        from wexample_prompt.responses.progress_prompt_response import ProgressPromptResponse

        """Execute all steps and return their results.
        
        Returns:
            List of results from each step
        
        Raises:
            Exception: If any step fails
        """
        results = []
        
        for step in self.steps:
            # Update progress before step
            progress = ProgressPromptResponse.create(
                total=100,
                current=int(100 * self.current_weight / self.total_weight),
                width=self.width,
                label=f"{self.title}: {step.description}" if self.title else step.description
            )
            progress.print(end="\r", flush=True)
            
            # Execute step
            result = step.callback()
            if result is False:
                raise Exception(f"Step failed: {step.description}")
                
            results.append(result)
            
            # Update progress
            self.current_weight += step.weight
            
        # Show final progress
        progress = ProgressPromptResponse.create(
            total=100,
            current=100,
            width=self.width,
            label=f"{self.title}: Complete" if self.title else "Complete"
        )
        progress.print(end="\n", flush=True)
        
        return results
