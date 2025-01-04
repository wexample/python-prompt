#!/usr/bin/env python3
"""Demo script showcasing error handling features."""

import os
import sys
from typing import Dict, Any, Tuple, Optional
from functools import wraps

from wexample_prompt.io_manager import IOManager


def handle_errors(func):
    """Decorator to handle errors and return success status.
    
    Args:
        func: Function to wrap
        
    Returns:
        Wrapped function that returns (success, result)
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Tuple[bool, Optional[Any]]:
        try:
            result = func(*args, **kwargs)
            return True, result
        except Exception as e:
            return False, None
    return wrapper


def simulate_file_operation(filename: str) -> Dict[str, Any]:
    """Simulate a file operation that might fail.
    
    Args:
        filename: Name of the file to operate on
        
    Returns:
        Dict with operation results
        
    Raises:
        FileNotFoundError: If file doesn't exist
        PermissionError: If file isn't accessible
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")
    if filename.endswith('.locked'):
        raise PermissionError(f"Access denied to file: {filename}")
    return {"size": 1024, "type": "text/plain"}


@handle_errors
def demo_basic_errors() -> None:
    """Demonstrate basic error and warning messages."""
    io = IOManager()
    
    print("\n=== Basic Error Handling ===")
    
    # Simple error and warning
    io.error("Basic error message", trace=False)
    io.warning("Basic warning message")
    
    # Messages with parameters
    io.error(
        "Error processing {filename}",
        params={"filename": "data.txt"},
        trace=False
    )
    io.warning(
        "Resource usage at {percent}%",
        params={"percent": 85}
    )


@handle_errors
def demo_error_traces() -> None:
    """Demonstrate error handling with stack traces."""
    io = IOManager()
    
    print("\n=== Stack Traces ===")
    
    # Error with stack trace
    try:
        result = simulate_file_operation("nonexistent.txt")
    except FileNotFoundError as e:
        # Show error message without raising
        io.error(
            "File operation failed: {error}",
            params={"error": str(e)},
            trace=True
        )
        # Return without raising to prevent double traceback
        return
    
    # Warning with trace
    try:
        result = simulate_file_operation("config.locked")
    except PermissionError as e:
        io.warning(
            "Permission issue: {error}",
            params={"error": str(e)},
            trace=True
        )
        # Return without raising to prevent double traceback
        return


@handle_errors
def demo_nested_errors() -> None:
    """Demonstrate error handling in nested contexts."""
    io = IOManager()
    
    print("\n=== Nested Error Handling ===")
    
    io.info("Starting nested operation...")
    io._log_indent += 1
    
    try:
        raise ValueError("Invalid configuration")
    except ValueError as e:
        io.error(
            "Nested operation failed: {error}",
            params={"error": str(e)},
            trace=True
        )
    
    io._log_indent -= 1
    io.info("Nested operation complete")


@handle_errors
def demo_fatal_error() -> None:
    """Demonstrate fatal error handling (commented out)."""
    io = IOManager()
    
    print("\n=== Fatal Error Handling ===")
    io.info("About to demonstrate fatal error (commented out)...")
    
    # Uncomment to see fatal error behavior:
    # io.error(
    #     "Critical system error",
    #     fatal=True,
    #     exit_code=1
    # )


def run_demos() -> bool:
    """Run all demos and return overall success status.
    
    Returns:
        True if all demos succeeded, False otherwise
    """
    demos = [
        ("Basic Error Handling", demo_basic_errors),
        ("Error Traces", demo_error_traces),
        ("Nested Errors", demo_nested_errors),
        ("Fatal Error", demo_fatal_error)
    ]
    
    io = IOManager()
    all_succeeded = True
    
    print("=== Error Handling Demo ===")
    
    for name, demo in demos:
        success, _ = demo()
        if not success:
            io.error(f"Demo '{name}' failed", trace=False)
            all_succeeded = False
    
    if all_succeeded:
        io.success("\nAll demos completed successfully!")
    else:
        io.error("\nSome demos failed", trace=False)
    
    return all_succeeded


if __name__ == "__main__":
    success = run_demos()
    sys.exit(0 if success else 1)
