"""Text width calculation utilities for proper display width including emojis."""

from __future__ import annotations

import wcwidth


def get_visible_width(text: str) -> int:
    """Calculate the visible width of text using wcwidth.
    
    This function properly handles:
    - Regular ASCII characters (width 1)
    - Emojis and other wide characters (width 2)
    - Zero-width characters (width 0)
    - ANSI escape codes are NOT handled here - strip them first with ansi_strip()
    
    Args:
        text: The text to measure (should be ANSI-stripped)
        
    Returns:
        The visible width in terminal columns
    """
    width = wcwidth.wcswidth(text)
    # wcswidth returns -1 if the string contains non-printable characters
    # In that case, fall back to character-by-character calculation
    if width == -1:
        width = 0
        for char in text:
            char_width = wcwidth.wcwidth(char)
            # wcwidth returns -1 for control characters, treat as 0
            if char_width == -1:
                char_width = 0
            width += char_width
    
    return max(0, width)
