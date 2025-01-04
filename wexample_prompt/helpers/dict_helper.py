"""Helper functions for dictionary operations."""
from typing import Dict, TypeVar

K = TypeVar('K')
V = TypeVar('V')


def dict_merge(dict1: Dict[K, V], dict2: Dict[K, V]) -> Dict[K, V]:
    """Merge two dictionaries.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary
        
    Returns:
        Dict: Merged dictionary
    """
    return {**dict1, **dict2}


def dict_sort_values(d: Dict[K, V]) -> Dict[K, V]:
    """Sort dictionary by values.
    
    Args:
        d: Dictionary to sort
        
    Returns:
        Dict: New dictionary sorted by values
    """
    return dict(sorted(d.items(), key=lambda x: str(x[1])))
