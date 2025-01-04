"""Main title response implementation."""
from wexample_prompt.responses.titles.base_title_response import BaseTitleResponse


class MainTitleResponse(BaseTitleResponse):
    """Response for main titles with arrow prefix."""
    
    @classmethod
    def get_prefix(cls) -> str:
        """Get the prefix for main titles.
        
        Returns:
            str: The main title prefix (▶)
        """
        return "▶"
