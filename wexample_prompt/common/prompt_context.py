import shutil
from typing import Optional
from pydantic import BaseModel, Field


class PromptContext(BaseModel):
    """Context for rendering responses, including terminal information."""
    terminal_width: int = Field(
        default_factory=lambda: shutil.get_terminal_size().columns
    )
    is_tty: bool = Field(
        default_factory=lambda: hasattr(shutil.sys.stdout, 'isatty') 
        and shutil.sys.stdout.isatty()
    )
    color_enabled: bool = Field(default=True)
    indentation: int = Field(default=0)  # Number of indentation levels
    
    def get_effective_width(self) -> int:
        """Get the effective width considering terminal constraints."""
        return min(self.terminal_width, 120)  # Cap at reasonable width
        
    def should_use_color(self) -> bool:
        """Determine if color should be used."""
        return self.color_enabled and self.is_tty
        
    def get_indentation(self) -> str:
        """Get the current indentation string."""
        return "  " * self.indentation  # Two spaces per level
