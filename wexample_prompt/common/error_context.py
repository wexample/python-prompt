"""Error context for error handling."""
from typing import Optional, Dict, Any

from wexample_prompt.common.prompt_context import PromptContext


class ErrorContext(PromptContext):
    """Context for error handling.
    
    This class holds information about how an error should be handled:
    - trace: If True, include stack trace in output
    - params: Optional parameters for message formatting
    """
    
    trace: bool = True
    params: Optional[Dict[str, Any]] = None
    
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
