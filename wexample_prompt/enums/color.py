from enum import Enum
from typing import Any, Type


class Color(Enum):
    """ANSI color codes for terminal output."""
    
    # Standard colors
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[0;33m"
    BLUE = "\033[0;34m"
    MAGENTA = "\033[0;35m"
    CYAN = "\033[0;36m"
    WHITE = "\033[0;37m"
    
    # Light colors
    LIGHT_RED = "\033[0;91m"
    LIGHT_GREEN = "\033[0;92m"
    LIGHT_YELLOW = "\033[0;93m"
    LIGHT_BLUE = "\033[0;94m"
    LIGHT_MAGENTA = "\033[0;95m"
    LIGHT_CYAN = "\033[0;96m"
    
    # Special colors
    GRAY = "\033[0;90m"
    LIGHT_GRAY = "\033[0;37m"
    DEFAULT = "\033[0m"
    RESET = "\033[0m"
    
    @classmethod
    def get_color(cls, name: str) -> Type["Color"[Any]] | "Color":
        """Get color by name, case-insensitive."""
        try:
            return cls[name.upper()]
        except KeyError:
            return cls.DEFAULT
            
    def __str__(self) -> str:
        """Return the ANSI code when converting to string."""
        return self.value
