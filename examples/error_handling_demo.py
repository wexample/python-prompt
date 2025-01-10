#!/usr/bin/env python3
"""Demo script showcasing error handling features."""

import os
import sys
from typing import Dict, Any, Tuple, Optional
from functools import wraps

from wexample_prompt.io_manager import IoManager
from wexample_prompt.responses import MainTitleResponse
from wexample_prompt.responses.messages import InfoPromptResponse


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
def demo_basic_errors(io: IoManager) -> None:
    """Demonstrate basic error and warning messages."""
    title = MainTitleResponse.create("Basic Error Handling")
    io.print_response(title)
    
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
def demo_error_traces(io: IoManager) -> None:
    """Demonstrate error handling with stack traces."""
    title = MainTitleResponse.create("Stack Traces")
    io.print_response(title)
    
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


@handle_errors
def demo_nested_errors(io: IoManager) -> None:
    """Demonstrate error handling in nested contexts."""
    title = MainTitleResponse.create("Nested Error Handling")
    io.print_response(title)
    
    try:
        # Outer operation
        io.info("Starting outer operation...")
        try:
            # Inner operation that fails
            result = simulate_file_operation("inner/data.locked")
        except PermissionError as e:
            # Handle inner error
            io.error(
                "Inner operation failed: {error}",
                params={"error": str(e)},
                trace=True
            )
            raise  # Re-raise to trigger outer handler
    except Exception as e:
        # Handle outer error
        io.error(
            "Outer operation failed: {error}",
            params={"error": str(e)},
            trace=True
        )


@handle_errors
def demo_fatal_error(io: IoManager) -> None:
    """Demonstrate fatal error handling."""
    title = MainTitleResponse.create("Fatal Error Handling")
    io.print_response(title)
    
    io.info("This demo is skipped to prevent program termination")
    io.info("In real usage, fatal=True would terminate the program")
    
    # Commented out to prevent actual termination
    # io.error(
    #     "Fatal error occurred",
    #     fatal=True,
    #     trace=True
    # )


def run_demos() -> bool:
    """Run all demos and return overall success status.
    
    Returns:
        True if all demos succeeded, False otherwise
    """
    io = IoManager()
    
    title = MainTitleResponse.create("Error Handling Demo")
    io.print_response(title)
    
    demos = [
        ("Basic Error Handling", demo_basic_errors),
        ("Stack Traces", demo_error_traces),
        ("Nested Error Handling", demo_nested_errors),
        ("Fatal Error Handling", demo_fatal_error)
    ]
    
    success = True
    for name, demo in demos:
        io.print_response(InfoPromptResponse.create(f"\nRunning {name}..."))
        demo_success, _ = demo(io)
        if not demo_success:
            success = False
            io.error(f"Demo '{name}' failed")
    
    if success:
        io.success("\nAll demos completed successfully")
    else:
        io.error("\nSome demos failed", trace=False)
    
    return success


if __name__ == "__main__":
    success = run_demos()
    sys.exit(0 if success else 1)
