"""Error context for error handling."""
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class ErrorContext:
    """Context for error handling.
    
    This class holds information about how an error should be handled:
    - fatal: If True, the error should stop execution
    - trace: If True, include stack trace in output
    - params: Optional parameters for message formatting
    - exit_code: Exit code to use when fatal is True
    """
    
    fatal: bool = False
    trace: bool = True
    params: Optional[Dict[str, Any]] = None
    exit_code: int = 1
    
    def format_message(self, message: str) -> str:
        """Format message with parameters if any.
        
        Args:
            message: Message template
            
        Returns:
            Formatted message
        """
        if self.params:
            return message.format(**self.params)
        return message
